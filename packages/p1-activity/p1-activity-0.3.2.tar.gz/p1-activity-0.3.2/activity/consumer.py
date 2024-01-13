from builtins import str

from p1_queue.base_consumer import BaseConsumer

from activity.constants import K_TRIGGER_PROCESS_ON_CREATE
from activity.constants import K_TRIGGER_PROCESS_ON_DELETE
from activity.constants import K_TRIGGER_PROCESS_ON_UPDATE
from activity.constants import K_TRIGGER_ACTIVITY_ON_COMPLETE
from activity.constants import K_TRIGGER_ACTIVITY_ON_CREATE
from activity.constants import K_TRIGGER_ACTIVITY_ON_DELETE
from activity.constants import K_TRIGGER_ACTIVITY_ON_UPDATE
from activity.constants import K_TRIGGER_ACTIVITY_SUBMISSION_ON_UNSUBMIT
from activity.constants import K_TRIGGER_ACTIVITY_SUBMISSION_ON_SUBMIT
from activity.constants import K_TRIGGER_ACTIVITIES_REMINDER_ON_SEND
from activity.services import BaseConsumerService


class BaseActivityConsumer(BaseConsumer):
    TOPIC_ID = None

    consumer_service = None

    def get_consumer_service(self):
        if self.consumer_service is None:
            raise NotImplementedError('No consumer service')
        if not issubclass(type(self.consumer_service), BaseConsumerService):
            raise ValueError(
                'Consumer service not inherit from BaseConsumerService')
        return self.consumer_service

    def perform_on_process_created(self, data):
        self.get_consumer_service() \
            .on_process_created(data['process'])

    def perform_on_process_updated(self, data):
        self.get_consumer_service() \
            .on_process_updated(data['process'])

    def perform_on_process_deleted(self, data):
        self.get_consumer_service() \
            .on_process_deleted(data['process'])

    def perform_on_activity_completed(self, data):
        self.get_consumer_service() \
            .on_activity_completed(data['activity'])

    def perform_on_activity_created(self, data):
        self.get_consumer_service() \
            .on_activity_created(data['activity'])

    def perform_on_activity_updated(self, data):
        self.get_consumer_service() \
            .on_activity_updated(data['activity'])

    def perform_on_activity_deleted(self, data):
        self.get_consumer_service() \
            .on_activity_deleted(data['activity'])

    def perform_on_submission_submitted(self, data):
        self.get_consumer_service() \
            .on_activity_submission_submitted(
            data['activity_submission'], data['activity'])

    def perform_on_submission_unsubmitted(self, data):
        self.get_consumer_service() \
            .on_activity_submission_unsubmitted(
            data['activity_submission'], data['activity'])

    def perform_on_activities_reminder_sent(self, data):
        self.get_consumer_service() \
            .on_activities_reminder_sent(
            data['activities_by_remaining_days'])

    def perform_on_value_error(self, error):
        self.get_consumer_service() \
            .on_value_error(error)

    def perform_on_internal_server_error(self, error, message_id, data, attributes, published_time):
        self.get_consumer_service() \
            .on_internal_server_error(error, message_id, data, attributes, published_time)

    def validate_trigger_type(self, attributes):
        if attributes['trigger_type'] == '':
            raise ValueError({'trigger_type': 'missing trigger_type'})
        return attributes['trigger_type']

    def on_message(self, message_id, data, attributes, published_time):
        try:
            trigger_type = self.validate_trigger_type(attributes)

            if trigger_type == K_TRIGGER_PROCESS_ON_CREATE:
                self.perform_on_process_created(data)
            elif trigger_type == K_TRIGGER_PROCESS_ON_UPDATE:
                self.perform_on_process_updated(data)
            elif trigger_type == K_TRIGGER_PROCESS_ON_DELETE:
                self.perform_on_process_deleted(data)
            elif trigger_type == K_TRIGGER_ACTIVITY_ON_COMPLETE:
                self.perform_on_activity_completed(data)
            elif trigger_type == K_TRIGGER_ACTIVITY_ON_CREATE:
                self.perform_on_activity_created(data)
            elif trigger_type == K_TRIGGER_ACTIVITY_ON_UPDATE:
                self.perform_on_activity_updated(data)
            elif trigger_type == K_TRIGGER_ACTIVITY_ON_DELETE:
                self.perform_on_activity_deleted(data)
            elif trigger_type == K_TRIGGER_ACTIVITY_SUBMISSION_ON_SUBMIT:
                self.perform_on_submission_submitted(data)
            elif trigger_type == K_TRIGGER_ACTIVITY_SUBMISSION_ON_UNSUBMIT:
                self.perform_on_submission_unsubmitted(data)
            elif trigger_type == K_TRIGGER_ACTIVITIES_REMINDER_ON_SEND:
                self.perform_on_activities_reminder_sent(data)
            else:
                raise ValueError({'trigger_type': 'invalid trigger_type'})
        except ValueError as e:
            self.perform_on_value_error(e)
        except Exception as e:
            self.perform_on_internal_server_error(
                e, message_id, data, attributes, published_time)
