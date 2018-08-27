class Util(object):
    """
    Contains useful utility functions outside of the core and project API.
    """

    def __init__(self, webgme):
        self._webgme = webgme
        self._gme_config = None

    def _send(self, payload):
        payload['type'] = 'util'
        self._webgme.send_request(payload)
        return self._webgme.handle_response()

    @property
    def gme_config(self):
        """
        The gmeConfig in form of a dictionary.
        """
        if self._gme_config is None:
            self._gme_config = self._send({'name': 'gmeConfig', 'args': []})

        return self._gme_config

    def save(self, root_node, commit_hash, branch_name=None, msg='Save initiated from python api.'):
        """
        Persists the core tree from root node and makes a commit to the database.
        This method is short-hand for (and does not send all persisted objects over zeromq):

        persisted = webgme.core.persist(root_node)
        webgme.project.make_commit(branch_name, [commit_hash], persisted['rootHash'], persisted['objects'], msg)

        :param root_node: root of core tree that should be persisted and committed.
        :type root_node: dict
        :param commit_hash: commit-hash from where the now mutated root node came from
        :type commit_hash: str
        :param branch_name: Name of branch to update (will only insert a commit if not given).
        :type branch_name: str
        :param msg: Commit message.
        :type msg: str
        :returns: Status about the commit and branch update (same as project.makeCommit)
        :rtype: dict
        :raises JSError: The result of the execution.
        :raises CoreIllegalArgumentError: If the supplied root_node is of wrong format
        """
        return self._send({
            'name': 'save',
            'args': [root_node, commit_hash, branch_name, msg]
        })

    def unload_root(self, node):
        """
        Removes the reference to the root node associated with the node inside the corezmq.js module allowing
        the tree to be garbage collected. This should typically not be needed as the typical usage of
        the bindings is to load and work with one (or two roots) and then terminate the corezmq.js server.

        :param node: any node in a core tree
        :type node: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises JSError: The result of the execution.
        """
        self._send({
            'name': 'unloadRoot',
            'args': [node]
        })

    def META(self, node, namespace=None):
        """
        Gathers the and returns the meta nodes in the core tree associated with the node.
        If a namespace is supplied, only meta-nodes part of the corresponding library are returned.

        Note that the names are fully-qualified (relative the provided namespace).

        :param node:
        :type node: dict
        :param namespace:
        :type namespace: str
        :return: Dictionary where keys are the names of the meta-nodes (the equivalent of the native plugin.META)
        :rtype: dict
        :raises JSError: The result of the execution.
        :raises CoreIllegalArgumentError: If the supplied node is of wrong format
        """
        return self._send({
            'name': 'META',
            'args': [node, namespace]
        })

    def equal(self, node1, node2):
        """
        Check if two node dicts represent the same node.
        :param node1:
        :type node1: dict
        :param node2:
        :type node2: dict
        :return: True if the nodes are equal
        :rtype: bool
        """
        return node1['nodePath'] == node2['nodePath'] and node1['rootId'] == node2['rootId']