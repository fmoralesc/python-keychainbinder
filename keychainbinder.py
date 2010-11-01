#!/usr/bin/env python
"""some functions to bind globally available key sequences to callable objects."""

import gobject
import keybinder

def bind_keychain(chain, callback, timeout=400):
	"""Bind a callable object to a globally available key sequence.
	
	Arguments:
	chain		-- a string describing the key sequence.
	callback	-- a callable object
	timeout		-- how much time to wait before unbinding. (default: 400ms)
	"""
	def bind_tails(chain, callback, timeout):
		links = chain.split("-")
		head = links[0]
		tails = links[1:]
		if links != ['']:
			keybinder.bind(head, lambda : bind_tails("-".join(tails), callback, timeout))
			gobject.timeout_add(timeout, lambda : keybinder.unbind(head))
		else:
			callback()

	links = chain.split("-")
	head = links[0]
	tails = links[1:]
	keybinder.bind(head, lambda : bind_tails("-".join(tails), callback, timeout))

def bind_keychainset(head, keys, callbacks, timeout=400):
	"""Bind a set of key sequences with a common base to a set of functions.
	
	Arguments:
	head		-- the common base of the bindings. can be any sequence bindable by bind_keychain.
	keys		-- a set of keys to append to head to form a key sequence
	callbacks	-- a set of callable objects to map to keys
	timeout		-- how much time to wait before unbinding. (default: 400ms)
	"""
	def bind_choices(keys, callbacks, timeout):
		for (key, callback) in zip(keys, callbacks):
			bind_keychain(key, callback, timeout)
			gobject.timeout_add(timeout, lambda key=key: keybinder.unbind(key))

	bind_keychain(head, lambda: bind_choices(keys, callbacks, timeout), timeout)
