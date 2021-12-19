from django.http import HttpResponse

def main(request):
    return HttpResponse("""
    <a href="/blog">
        <h1>Blog</h1>
    </a>
    <a href="/store">
        <h1>Store</h1>
    </a>
    """)