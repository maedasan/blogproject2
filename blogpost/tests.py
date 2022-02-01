from django.test import TestCase
from .forms import CommentCreateForm, BlogCreateForm
import os.path
from django.core.files.uploadedfile import SimpleUploadedFile



##### コメントフォームのテスト
class CommentCreateFormTests(TestCase):
####### 正常動作確認
    def test_correct_form(self):
        comment_data = {
            'user_name' : '大塚愛',
            'message' : 'はじめまして、初めて日記読まさせて頂きました。',
            }
        form = CommentCreateForm(comment_data)
        self.assertTrue(form.is_valid())



####### エラーになるパターン user_name(コメント投稿者)が空白の場合
    def test_error_username_form(self):
        comment_data = {
            'user_name' : '',
            'message' : 'はじめまして、初めて日記読まさせて頂きました。',
            }
        form = CommentCreateForm(comment_data)
        self.assertEqual(form.errors['user_name'],['This field is required.'])
        self.assertFalse(form.is_valid())



####### エラーになるパターン message(コメント本文)が空白の場合
    def test_error_message_form(self):
        comment_data = {
            'user_name' : '大塚愛',
            'message' : '',
            }
        form = CommentCreateForm(comment_data)
        self.assertEqual(form.errors['message'],['This field is required.'])
        self.assertFalse(form.is_valid())





class BlogCreateFormTests(TestCase):
####### 正常動作確認
    def test_normally(self):
        form_data = {
            'title': 'こんにちは',
            'content': 'おはようございます。',
            }

        # 添付ファイルデータ
        image_file_path = './tests/fixtures/sample.png'
        with open(image_file_path, 'rb') as f:
            image_file_data = f.read()
        attach_files = {
            'images': SimpleUploadedFile(image_file_path, image_file_data)
            }

        form = BlogCreateForm(form_data, attach_files)
        self.assertTrue(form.is_valid())




class abcTest(TestCase):
    
    def test_abc(self):
        if(os.path.isfile('./blogpost/tenki1.jpg') == True):
            print('ファイルは存在します')
        else:
            print('ファイルは存在しません')

