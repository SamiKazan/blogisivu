import bleach
import re

#Check content for non permitted tags and remove excess br tags
def sanitize_and_convert_newlines(content):
    allowed_tags = ['i', 'u', 'ul', 'ol', 'li', 'strong', 'br']
    
    sanitized_content = bleach.clean(content, tags=allowed_tags, strip=True)
    
    sanitized_content = sanitized_content.replace('\r\n', '<br>').replace('\n', '<br>')
    
    sanitized_content = re.sub(r'(<br\s*/?>\s*){3,}', '<br><br>', sanitized_content)

    return sanitized_content