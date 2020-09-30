# -*- coding: utf-8 -*-

from robot.api import logger
from robot.utils import ConnectionCache
import http.client
import base64
import json
import socket
import urllib.parse
import urllib


class RabbitMqCustom(object):
    """
    Library for managing the server RabbitMq.

    == Example ==
    | *Settings* | *Value* |
    | Library    |       RabbitMqManager |
    | Library     |      Collections |

    | *Test Cases* | *Action* | *Argument* | *Argument* | *Argument* | *Argument* | *Argument* |
    | Simple |
    |    | Connect To Rabbitmq | my_host_name | 15672 | guest | guest | alias=rmq |
    |    | ${overview}= | Overview |
    |    | Log Dictionary | ${overview} |
    |    | Close All Rabbitmq Connections |
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._connection = None
        self.headers = None
        self._cache = ConnectionCache()

    def connect_to_rabbitmq(self, host, port, username='guest', password='guest', timeout=15, alias=None):
        """
        Connecting to the server RabbitMq.

        *Args:*\n
        _host_ - server name;\n
        _port_ - port number;\n
        _username_ - is the name of the user;\n
        _password_ - is the user password;\n
        _timeout_ - connection timeout;\n
        _alias_ - connection alias;\n

        *Returns:*\n
        The index of the current connection.

        *Raises:*\n
        socket.error if you can not create a connection.

        *Example:*\n
        | Connect To Rabbitmq | my_host_name | 15672 | guest | guest | alias=rmq |
        """

        port = int(port)
        timeout = int(timeout)
        logger.debug('Connecting using : host=%s, port=%d, username=%s, password=%s, timeout=%d, alias=%s ' % (
            host, port, username, password, timeout, alias))
        self.headers = {"Authorization": b"Basic " +
                        base64.b64encode(username.encode() + b":" + password.encode())}
        logger.debug(self.headers)
        try:
            self._connection = http.client.HTTPConnection(host, port, timeout)
            self._connection.connect()
            return self._cache.register(self._connection, alias)
        except socket.error as e:
            raise Exception("Could not connect to RabbitMq", str(e))

    def switch_rabbitmq_connection(self, index_or_alias):
        """
        Switch between active connections with RabbitMq, using their index or alias..

        The alias is specified in the keyword [#Connect To Rabbitmq|Connect To Rabbitmq], which also returns the connection index.

        *Args:*\n
        _index_or_alias_ - index of a connection or its alias;

        *Returns:*\n
        Index of the previous connection..

        *Example:*\n
        | Connect To Rabbitmq | my_host_name_1 | 15672 | guest | guest | alias=rmq1 |
        | Connect To Rabbitmq | my_host_name_2 | 15672 | guest | guest | alias=rmq2 |
        | Switch Rabbitmq Connection | rmq1 |
        | ${live}= | Is alive |
        | Switch Rabbitmq Connection | rmq2 |
        | ${live}= | Is alive |
        | Close All Rabbitmq Connections |
        """

        old_index = self._cache.current_index
        self._connection = self._cache.switch(index_or_alias)
        return old_index

    def disconnect_from_rabbitmq(self):
        """
        Closing the current connection to RabbitMq.

        *Example:*\n
        | Connect To Rabbitmq | my_host_name | 15672 | guest | guest | alias=rmq |
        | Disconnect From Rabbitmq |
        """

        logger.debug('Close connection with : host=%s, port=%d  ' %
                     (self._connection.host, self._connection.port))
        self._connection.close()

    def close_all_rabbitmq_connections(self):
        """
        Closing all connections from RabbitMq..

        This keyword is used to close all connections in the event that several of them were opened.
        Use [#Disconnect From Rabbitmq|Disconnect From Rabbitmq] и [#Close All Rabbitmq Connections|Close All Rabbitmq Connections]
        together it is impossible..

        After this keyword is executed, the index returned by [#Connect To Rabbitmq|Connect To Rabbitmq], starts at 1.

        *Example:*\n
        | Connect To Rabbitmq | my_host_name | 15672 | guest | guest | alias=rmq |
        | Close All Rabbitmq Connections |
        """

        self._connection = self._cache.close_all()

    def _http_request(self, method, path, body):
        """
        Querying for RabbitMq

        *Args:*\n
        _method_ - query method;\n
        _path_ - uri request;\n
        _body_ - body POST request;\n
        """

        if body != "":
            self.headers["Content-Type"] = "application/json"

        logger.debug('Prepared request with method ' + method + ' to ' + 'http://' +
                     self._connection.host + ':' + str(self._connection.port) + path + ' and body\n' + body)

        try:
			# TODO: analiser o funcionamento do cache de conexão
			# precisa recriar a toda hora?
            self._connection = http.client.HTTPConnection(
                self._connection.host, self._connection.port,
                self._connection.timeout)
            self._connection.connect()

            self._connection.request(method, path, body, self.headers)
        except socket.error as e:
            raise Exception("Could not send request: {0}".format(e))

        resp = self._connection.getresponse()
        s = resp.read()

        if resp.status == 400:
            raise Exception(json.loads(s))
        if resp.status == 401:
            raise Exception("Access refused: {0}".format(
                'http://' + self._connection.host + ':' + str(self._connection.port) + path))
        if resp.status == 404:
            raise Exception("Not found: {0}".format(
                'http://' + self._connection.host + ':' + str(self._connection.port) + path))
        if resp.status == 301:
            url = urllib.parse.urlparse(resp.getheader('location'))
            raise Exception(url)
            [host, port] = url.netloc.split(':')
            self.options.hostname = host
            self.options.port = int(port)
            return self.http(method, url.path + '?' + url.query, body)
        if resp.status < 200 or resp.status > 400:
            raise Exception("Received %d %s for request %s\n%s"
                            % (resp.status, resp.reason, 'http://' + self._connection.host + ':' + str(self._connection.port) + path, resp.read()))
        return s

    def _get(self, path):
        return self._http_request('GET', '/api%s' % path, '')

    def _put(self, path, body):
        print("/api%s" % path)
        return self._http_request("PUT", "/api%s" % path, body)

    def _post(self, path, body):
        return self._http_request("POST", "/api%s" % path, body)

    def _delete(self, path):
        return self._http_request("DELETE", "/api%s" % path, "")

    def _quote_vhost(self, vhost):
        """
        Decodificação vhost.
        """

        if vhost == '/':
            vhost = '%2F'
        if vhost != '%2F':
            vhost = urllib.parse.quote(vhost)
        return vhost

    def is_alive(self):
        """
        RabbitMq health check..

        The GET request is sent as follows: 'http://<host>:<port>/api/' and the return code is checked.

        *Returns:*\n
        bool True, if the return code is 200.\n
        bool False in all other cases.

        *Raises:*\n
        socket.error in case it is unreasonable to send a GET request.

        *Example:*\n
        | ${live}=  |  Is Alive |
        =>\n
        True
        """

        try:
            self._get('/cluster-name')
        except Exception:
            return False

        return True

    def overview(self):
        """
        Information about the server RabbitMq.

        *Returns:*\n
        Dictionary with information about the server.

        *Example:*\n
        | ${overview}=  |  Overview |
        | Log Dictionary  |  ${overview} |
        | ${version}=  |  Get From Dictionary | ${overview}  |  rabbitmq_version |
        =>\n
        Dictionary size is 13 and it contains following items:
        | erlang_full_version | Erlang R16B02 (erts-5.10.3) [source] [64-bit] [smp:2:2] [async-threads:30] [hipe] [kernel-poll:true] |
        | erlang_version | R16B02 |
        | listeners | [{u'node': u'rabbit@srv2-rs582b-m', u'ip_address': u'0.0.0.0', u'protocol': u'amqp', u'port': 5672}] |
        | management_version | 3.6.6 |
        | message_stats | [] |

        ${version} = 3.6.6
        """

        return json.loads(self._get('/overview'))

    def connections(self):
        """
        A list of open connections..
        """

        return json.loads(self._get('/connections'))

    def get_name_of_all_connections(self):
        """
        A list of the names of all open connections.
        """

        names = []
        data = self.connections()
        for item in data:
            names.append(item['name'])
        return names

    def channels(self):
        """
        List of open channels.
        """

        return json.loads(self._get('/channels'))

    def exchanges(self):
        """
        Exchange list.

        *Example:*\n
        | ${exchanges}=  |  Exchanges |
        | Log List  |  ${exchanges} |
        | ${item}=  |  Get From list  |  ${exchanges}  |  1 |
        | ${name}=  |  Get From Dictionary  |  ${q}  |  name  |
        =>\n
        List length is 8 and it contains following items:
        | 0 | {u'name': u'', u'durable': True, u'vhost': u'/', u'internal': False, u'message_stats': [], u'arguments': {}, u'type': u'direct', u'auto_delete': False} |
        | 1 | {u'name': u'amq.direct', u'durable': True, u'vhost': u'/', u'internal': False, u'message_stats': [], u'arguments': {}, u'type': u'direct', u'auto_delete': False} |
        ...\n
        ${name} = amq.direct
        """

        return json.loads(self._get('/exchanges'))

    def get_names_of_all_exchanges(self):
        """
        List of names of all exchanges.

        *Example:*\n
        | ${names}=  |  Get Names Of All Exchanges |
        | Log List  |  ${names} |
        =>\n
        | List has one item:
        | amq.direct
        """

        names = []
        data = self.exchanges()
        for item in data:
            names.append(item['name'])
        return names

    def queues(self):
        """
        List of queues.
        """

        return json.loads(self._get('/queues'))

    def get_queues_on_vhost(self, vhost='%2F'):
        """
        List of queues for the virtual host.

        *Args:*\n
        _vhost_ -the name of the virtual host (recoded using urllib.parse.quote)
        """

        return json.loads(self._get('/queues/' + self._quote_vhost(vhost)))

    def get_queue(self, name, vhost='%2F'):
        """
        List of queues for the virtual host.

        *Args:*\n
        _queue_name_ - queue name;\n
        _vhost_ - the name of the virtual host (recoded using urllib.parse.quote)
        """

        return json.loads(self._get('/queues/' + self._quote_vhost(vhost) + '/' + urllib.parse.quote(name)))

    def get_names_of_queues_on_vhost(self, vhost='%2F'):
        """
        List of virtual host queue names.

        *Args:*\n
        - vhost: the name of the virtual host (recoded using urllib.parse.quote)

        *Example:*\n
        | ${names}=  |  Get Names Of Queues On Vhost |
        | Log List  |  ${names} |
        =>\n
        | List has one item:
        | federation: ex2 -> rabbit@server.br
        """
        names = []
        data = self.get_queues_on_vhost(vhost)
        for item in data:
            names.append(item['name'])
        return names

    def queue_exists(self, queue, vhost='%2F'):
        """
        Verifies that the one or more queues exists
        """
        names = self.get_names_of_queues_on_vhost()
        if queue in names:
            return True
        else:
            return False

    def delete_queues_by_name(self, name, vhost='%2F'):
        """
        Remove the queue from the virtual host.

        *Args:*\n
        _name_ -  is the name of the queue;\n
        _vhost_ - is the name of the virtual host;\n
        """
        print('Deletando a fila: %s' % (name))
        return self._delete('/queues/' + self._quote_vhost(vhost) + '/' + urllib.parse.quote(name))

    def vhosts(self):
        """
        List of virtual hosts.
        """
        return json.loads(self._get('/vhosts'))

    def nodes(self):
        """
        List of nodes in the RabbitMQ cluster
        """
        return json.loads(self._get('/nodes'))

    @property
    def _cluster_name(self):
        """
        Name identifying this RabbitMQ cluster.
        """
        return json.loads(self._get('/cluster-name'))

    def create_queues_by_name(self, name, auto_delete=False, durable=True, arguments={}, vhost='%2F'):
        """
        Create an individual queue.
        """
        print('Criando a fila: %s' % (name))
        node = self._cluster_name['name']
        body = json.dumps({
            "auto_delete": auto_delete,
            "durable": "true",
            "arguments": arguments,
            "node": node
        })
        print("Body: %s" % body)
        print('/queues/' + self._quote_vhost(vhost) + '/' + urllib.parse.quote(name))
        return self._put('/queues/' + self._quote_vhost(vhost) + '/' + urllib.parse.quote(name), body=body)

    def publish_message_by_name(self, queue, msg, properties, vhost='%2F'):
        """
        Publish a message to a given exchange
        """

        name = "amq.default"
        body = json.dumps({
            "properties": properties,
            "routing_key": queue,
            "payload": msg,
            "payload_encoding": "string"
        })
        routed = self._post('/exchanges/' + self._quote_vhost(vhost) +
                            '/' + urllib.parse.quote(name) + '/publish', body=body)
        print("Body Enviado: %s" % body)
        print("Fila Publicada: %s" % queue)
        return json.loads(routed)

    def get_messages_by_queue(self, queue, count=5, requeue=False, encoding="auto", truncate=2000000, vhost='%2F'):
        """
        Get messages from a queue.
        """

        print('Pegando %s mensagens da fila: %s' % (count, queue))
        body = json.dumps({
            "count":
            count,
            "requeue":
            requeue,
            "encoding":
            encoding,
            "truncate":
            truncate,
            "ackmode":
            "ack_requeue_true" if requeue else "ack_requeue_false"
        })
        messages = self._post('/queues/' + self._quote_vhost(vhost) +
                              '/' + urllib.parse.quote(queue) + '/get', body=body)
        return json.loads(messages)

    def purge_messages_by_queue(self, name, vhost='%2F'):
        """
        Purge contents of a queue.
        """
        print('Apagando as mensagens da fila: %s' % (name))
        return self._delete('/queues/' + self._quote_vhost(vhost) + '/' + urllib.parse.quote(name) + '/contents')
