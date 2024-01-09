"""
Application configuration constants and code.
"""

# .. toggle_name: EDX_DRF_EXTENSIONS[ENABLE_SET_REQUEST_USER_FOR_JWT_COOKIE]
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: Toggle for setting request.user with jwt cookie authentication. This makes the JWT cookie
#      user available to middleware while processing the request, if the session user wasn't already available. This
#      requires JwtAuthCookieMiddleware to work.
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2019-10-15
# .. toggle_target_removal_date: 2024-12-31
# .. toggle_warning: This feature caused a memory leak in edx-platform. This toggle is temporary only if we can make it
#      work in all services, or find a replacement. Consider making this a permanent toggle instead.
# .. toggle_tickets: ARCH-1210, ARCH-1199, ARCH-1197
ENABLE_SET_REQUEST_USER_FOR_JWT_COOKIE = 'ENABLE_SET_REQUEST_USER_FOR_JWT_COOKIE'

# .. toggle_name: EDX_DRF_EXTENSIONS[ENABLE_FORGIVING_JWT_COOKIES]
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: If True, return None rather than an exception when authentication fails with JWT cookies.
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2023-08-01
# .. toggle_target_removal_date: 2023-10-01
# .. toggle_tickets: https://github.com/openedx/edx-drf-extensions/issues/371
ENABLE_FORGIVING_JWT_COOKIES = 'ENABLE_FORGIVING_JWT_COOKIES'
