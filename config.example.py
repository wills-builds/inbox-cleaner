# Example configuration for unsubscriber
# Rename to config.py and customize

# Search query for finding emails
# Options:
# - 'category:promotions' - Only promotional emails
# - 'category:updates' - Only update emails  
# - 'category:promotions OR category:updates' - Both
# - 'from:specific@email.com' - Specific sender
# - 'older_than:30d' - Older than 30 days
SEARCH_QUERY = 'category:promotions OR category:updates'

# Maximum number of emails to scan per run
MAX_EMAILS = 500

# Label name for processed emails
LABEL_NAME = 'Auto-Unsubscribed'

# Whitelist - senders to never unsubscribe from
# Example: ['important@company.com', 'newsletter@trusted.com']
WHITELIST = []

# Blacklist - senders to always mark (even if no unsubscribe link)
# Example: ['spam@bad.com', 'marketing@annoying.com']
BLACKLIST = []

# Auto-archive emails after labeling
AUTO_ARCHIVE = False

# Delete emails after unsubscribe info is extracted
AUTO_DELETE = False
