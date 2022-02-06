from django.shortcuts import render

# Create your views here.
def main(request):
    blog_info = '''Fully featured blog with filtering based on tags, categories or number of views,
          pagination and rich-text editor. Create, Update and Delete posts only for authenticated users.'''
    store_info = '''E-commerce store with different categories and filtering based on categories, product types and sizes.
          Rating and comment system, similar products carousel, "Add to cart" functionality by storing product 
          instance id in session, coupon redeeming and payment gateway.'''
    api_info = '''Simple blog API with post and comment retrieve, create, update and delete views and User Create View 
            for returning an authentication token.'''
    api_links = '''<br>
          <a href="http://localhost:8000/api/posts/">http://localhost:8000/api/posts/</a><br>
          <a href="http://localhost:8000/api/comments/">http://localhost:8000/api/comments/</a><br>
          <a href="http://localhost:8000/api/comment-create/">http://localhost:8000/api/comment-create/</a><br>
          <a href="http://localhost:8000/api/comment-update/3">http://localhost:8000/api/comment-update{pk}</a><br>
          <a href="http://localhost:8000/api/post-create/">http://localhost:8000/api/post-create/</a><br>
          <a href="http://localhost:8000/api/post-update/3">http://localhost:8000/api/post-update/{pk}</a><br>
          <a href="http://localhost:8000/api/register/">http://localhost:8000/api/register/</a><br>'''

    return render(request, 'index/index.html', {"blog_info": blog_info, "store_info": store_info, "api_info": api_info, "api_links": api_links})