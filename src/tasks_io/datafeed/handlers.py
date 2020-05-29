from google.cloud import tasks_v2


# cloud_tasks_client = tasks_v2.CloudTasksClient()


def event_list(year: int):
    sv = Sitevar.get_by_id('apistatus')

    if not year:
        # If no specific year specific, enqueue tasks to fetch for the current season year through the max season year
        current_year = sv.contents['current_season']
        max_year = sv.contents['max_season']
    else:
        # Ahhhhh
        """
        df_config = Sitevar.get_or_insert('event_list_datafeed_config')
        df = DatafeedFMSAPI('v2.0')
        df2 = DatafeedFIRSTElasticSearch()

        fmsapi_events, event_list_districts = df.getEventList(year)
        if df_config.contents.get('enable_es') == True:
            elasticsearch_events = df2.getEventList(year)
        else:
            elasticsearch_events = []

        # All regular-season events can be inserted without any work involved.
        # We need to de-duplicate offseason events from the FRC Events API with a different code than the TBA event code
        fmsapi_events_offseason = [e for e in fmsapi_events if e.is_offseason]
        event_keys_to_put = set([e.key_name for e in fmsapi_events]) - set(
            [e.key_name for e in fmsapi_events_offseason])
        events_to_put = [e for e in fmsapi_events if e.key_name in event_keys_to_put]

        matched_offseason_events, new_offseason_events = \
            OffseasonEventHelper.categorize_offseasons(int(year), fmsapi_events_offseason)

        # For all matched offseason events, make sure the FIRST code matches the TBA FIRST code
        for tba_event, first_event in matched_offseason_events:
            tba_event.first_code = first_event.event_short
            events_to_put.append(tba_event)  # Update TBA events - discard the FIRST event

        # For all new offseason events we can't automatically match, create suggestions
        SuggestionCreator.createDummyOffseasonSuggestions(new_offseason_events)

        merged_events = EventManipulator.mergeModels(
            list(events_to_put),
            elasticsearch_events) if elasticsearch_events else list(
                events_to_put)
        events = EventManipulator.createOrUpdate(merged_events) or []

        fmsapi_districts = df.getDistrictList(year)
        merged_districts = DistrictManipulator.mergeModels(fmsapi_districts, event_list_districts)
        if merged_districts:
            districts = DistrictManipulator.createOrUpdate(merged_districts)
        else:
            districts = []

        # Fetch event details for each event
        for event in events:
            taskqueue.add(
                queue_name='datafeed',
                target='backend-tasks',
                url='/backend-tasks/get/event_details/'+event.key_name,
                method='GET'
            )

        template_values = {
            "events": events,
            "districts": districts,
        }

        if 'X-Appengine-Taskname' not in self.request.headers:  # Only write out if not in taskqueue
            path = os.path.join(os.path.dirname(__file__), '../templates/datafeeds/fms_event_list_get.html')
            self.response.out.write(template.render(path, template_values))
        """
        pass
