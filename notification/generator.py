# Scheduler

# Notification should have required fields:
# 1. notification_id
# 2. content_id
# And might have optional fields:
# 3. last_update
# 4. last_notification_send

def once_a_week_notification():
    """
    Send Notification about new movies & series at every Friday
    Gather info about huge amount of Users & Events, then create individual Notifications &
    put them into the Notification MQ
    :return:
    """

