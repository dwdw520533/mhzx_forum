def is_mobile(req):
    '''
    Determine whether the req is issued by a mobile browser.
    '''
    TABLET_AGENTS = ('tablet', 'ipad', 'xoom', 'playbook', 'kindle')
    user_agent = req.user_agent.string.lower()
    for tab in TABLET_AGENTS:
        if tab in user_agent:
            return False
    if 'mobile' in user_agent:
        return True
    if 'android' in user_agent:
        # Android with Chrome(if not with mobile) are not mobile browser.
        if 'chrome' in user_agent:
            return False
        return True
    return False
