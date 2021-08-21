from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category


# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_a = User.objects.create_user(username='a',password='aa11aa22')
        self.user_b = User.objects.create_user(username='b',password='bb11bb22')
        self.category_me = Category.objects.create(name='imme', slug='imme')
        self.category_you = Category.objects.create(name='youareyou', slug='youareyou')
        
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello Word. We are the world.',
            category=self.category_me,
            author=self.user_a,
        )
        
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_you,
            author=self.user_b,
        )
        
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='카테고리가 없을수 잇죠',
            author=self.user_b,
        )
        
    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_me.name} ({self.category_me.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_you.name} ({self.category_you.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)
    
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        
        logo_btn = navbar.find('a', text='Django')
        self.assertEqual(logo_btn.attrs['href'],'/')
        
        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'],'/')
        
        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'],'/blog/')
        
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'],'/about_me/')
        
    
    def test_post_list(self):
        self.assertEqual(Post.objects.count(),3)
        
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.navbar_test(soup)
        self.category_card_test(soup)
        
        main_area=soup.find('div', id='main-area')
        
        post_001_card = soup.find('div', id='post-1')
        self.assertIn(self.post_001.title,post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        
        post_002_card = soup.find('div', id='post-2')
        self.assertIn(self.post_002.title,post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        
        post_003_card = soup.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        
        self.assertIn(self.user_a.username.upper(), main_area.text)
        self.assertIn(self.user_b.username.upper(), main_area.text)
        
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(),0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        
        
    def test_post_detail(self):
        
        post_000 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the orld.',
            author=self.user_a,
        )
        
        self.assertEqual(post_000.get_absolute_url(), '/blog/1/')
        
        response = self.client.get(post_000.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.navbar_test(soup)
        
        self.assertIn(post_000.title, soup.title.text)
        
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_000.title, post_area.text)
        
        self.assertIn(self.user_a.username.upper(), main_area.text)       
        
        self.assertIn(post_000.content, post_area.text)

        