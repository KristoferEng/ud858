    @endpoints.method(CONF_POST_REQUEST, SessionForm,
            path='session/{websafeSessionKey}',
            http_method='PUT', name='updateSession')
    def updateSession(self, request):
        """Update session w/provided fields & return w/updated info."""
        return self._updateSessionObject(request)


    @endpoints.method(CONF_GET_REQUEST, SessionForm,
            path='session/{websafeSessionKey}',
            http_method='GET', name='getSession')
    def getSession(self, request):
        """Return requested session (by websafeSessionKey)."""
        # get Session object from request; bail if not found
        sess = ndb.Key(urlsafe=request.websafeSessionKey).get()
        if not sess:
            raise endpoints.NotFoundException(
                'No session found with key: %s' % request.websafeSessionKey)
        prof = sess.key.parent().get()
        # return SessionForm
        return self._copySessionToForm(sess, getattr(prof, 'displayName'))


    def _getQuery(self, request):
        """Return formatted query from the submitted filters."""
        q = Session.query()
        inequality_filter, filters = self._formatFilters(request.filters)

        # If exists, sort on inequality filter first
        if not inequality_filter:
            q = q.order(Session.name)
        else:
            q = q.order(ndb.GenericProperty(inequality_filter))
            q = q.order(Session.name)

        for filtr in filters:
            if filtr["field"] in ["month", "maxAttendees"]:
                filtr["value"] = int(filtr["value"])
            formatted_query = ndb.query.FilterNode(filtr["field"], filtr["operator"], filtr["value"])
            q = q.filter(formatted_query)
        return q


    def _formatFilters(self, filters):
        """Parse, check validity and format user supplied filters."""
        formatted_filters = []
        inequality_field = None

        for f in filters:
            filtr = {field.name: getattr(f, field.name) for field in f.all_fields()}

            try:
                filtr["field"] = FIELDS[filtr["field"]]
                filtr["operator"] = OPERATORS[filtr["operator"]]
            except KeyError:
                raise endpoints.BadRequestException("Filter contains invalid field or operator.")

            # Every operation except "=" is an inequality
            if filtr["operator"] != "=":
                # check if inequality operation has been used in previous filters
                # disallow the filter if inequality was performed on a different field before
                # track the field on which the inequality operation is performed
                if inequality_field and inequality_field != filtr["field"]:
                    raise endpoints.BadRequestException("Inequality filter is allowed on only one field.")
                else:
                    inequality_field = filtr["field"]

            formatted_filters.append(filtr)
        return (inequality_field, formatted_filters)


    @endpoints.method(SessionQueryForms, SessionForms,
            path='querySessions',
            http_method='POST',
            name='querySessions')
    def querySessions(self, request):
        """Query for sessions."""
        sessions = self._getQuery(request)

        # need to fetch organiser displayName from profiles
        # get all keys and use get_multi for speed
        organisers = [(ndb.Key(Profile, sess.organizerUserId)) for sess in sessions]
        profiles = ndb.get_multi(organisers)

        # put display names in a dict for easier fetching
        names = {}
        for profile in profiles:
            names[profile.key.id()] = profile.displayName

        # return individual SessionForm object per Session
        return SessionForms(
                items=[self._copySessionToForm(sess, names[sess.organizerUserId]) for sess in \
                sessions]
        )

