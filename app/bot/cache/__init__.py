from .attachments import AttachmentsMemoryCache
from .timeouts import TimeoutManager

attachments_cache = AttachmentsMemoryCache()
timeout_manager = TimeoutManager()