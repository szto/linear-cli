.PHONY: check
check:
	pants lint ::
	pants check ::

.PHONY: format
format:
	pants tailor ::
	pants fmt ::