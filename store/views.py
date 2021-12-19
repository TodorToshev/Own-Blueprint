from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'store/index.html')
def main2(request):
    return render(request, 'store/products.html')