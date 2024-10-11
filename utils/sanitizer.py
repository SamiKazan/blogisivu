import bleach

#Check content for non permitted tags
def sanitize_and_convert_newlines(content):
    # Allowed HTML tags and attributes
    allowed_tags = ['i', 'u', 'ul', 'ol', 'li', 'strong', 'br']
    
    sanitized_content = bleach.clean(content, tags=allowed_tags, strip=True)
    
    sanitized_content = sanitized_content.replace('\r\n', '<br>').replace('\n', '<br>')
    
    return sanitized_content