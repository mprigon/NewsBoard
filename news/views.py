from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView,\
    DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from .models import Post, Comment, Author, NewsLetter, Code
from .forms import NewsForm, CommentForm, NewsLetterForm, ConfirmationCodeForm
from .filters import CommentFilter


class PostList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'news_all.html'
    context_object_name = 'news'
    paginate_by = 10


class PostListSearch(ListView):
    model = Post
    ordering = '-time'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 4


class PostDetail(DetailView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'news_id'


class CommentDetail(DetailView):
    model = Comment
    template_name = 'comments_id.html'
    context_object_name = 'comments_id'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        # переопределение метода, чтобы добавить автора - текущего пользователя
        self.object = form.save(commit=False)
        print(f'user = {self.request.user} name = {self.request.user.username}')

        obj, created = Author.objects.get_or_create(
            authorUser=self.request.user
        )
        print(f'author = {self.request.user.author} obj = {obj}')
        self.object.author = obj
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.id = self.kwargs['pk']
        print(f'post.id = {post.id}')
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    raise_exception = True
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    context_object_name = 'news_id'


class CommentCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_comment')
    raise_exception = True
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        # переопределение метода, чтобы добавить commentUser - текущего пользователя

        # print(f'user = {self.request.user} name = {self.request.user.username}')
        comment = form.save(commit=False)
        comment.commentUser = self.request.user
        post_id = self.kwargs['pk']
        # print(f'pk = {post_id}')
        comment.commentPost = get_object_or_404(Post, id=post_id)
        # print(f'commentUser = {comment.commentUser}')
        # print(f'commentPost = {comment.commentPost}')

        return super().form_valid(form)


class CommentSearch(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_comment', 'news.add_post')
    raise_exception = True
    model = Comment
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'comment_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'comment_search'
    paginate_by = 4  # количество записей на странице

    # Переопределяем функцию получения списка откликов
    def get_queryset(self):
        queryset = super().get_queryset()
        # print(f'queryset до фильтра по текущему пользователю = {queryset}')

        user_current = self.request.user
        # print(f'текущий пользователь = {user_current}')
        # groups_of_current_user = user_current.groups.all().values_list('name', flat=True)
        # print(f'group = {groups_of_current_user}')

        post_by_current_user = Post.objects.filter(author=user_current.author)
        # print(f'post_by_current_user {post_by_current_user}')
        # commentPost_fields = queryset.values('commentPost')
        # print(f'commentPost_fields = {commentPost_fields}')

        queryset = queryset.filter(commentPost__in=post_by_current_user)
        # print(f'queryset после фильтра по текущему пользователю = {queryset}')

        # Возвращаем из функции отфильтрованный список откликов
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Метод get_context_data позволяет изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


@permission_required('news.delete_comment')
def comment_accept(request, pk):
    """Accept comment to author's post"""
    # print(f'comment_accept_view: pk = {pk}')
    comment_accepted = Comment.objects.get(id=pk)
    # print(f'comment_accepted = {comment_accepted}')
    comment_accepted.status = True
    # print(f'comment_accepted_status = {comment_accepted.status}')
    comment_accepted.save()
    message = 'Вы успешно приняли отклик на свое объявление'
    return render(request, 'comment_action_confirm.html', {'comment': comment_accepted, 'message': message})


@permission_required('news.delete_comment')
def comment_delete(request, pk):
    """Delete comment to author's post"""
    comment_to_delete = Comment.objects.get(id=pk)
    # print(f'до удаления: comment_to_delete = {comment_to_delete}')
    comment_to_delete.delete()
    message = 'Вы успешно удалили отклик на свое объявление'
    return render(request, 'comment_action_confirm.html', {'comment': comment_to_delete, 'message': message})


class CommentList(PermissionRequiredMixin, ListView):
    """Lists all accepted comments to a specific post. Page can be reached while reviewing a post."""

    permission_required = ('news.view_comment', 'news.view_post')
    raise_exception = True
    model = Comment
    ordering = '-dateCreation'
    context_object_name = 'comment_list'
    template_name = 'comment_list.html'
    paginate_by = 4

    # Переопределяем функцию получения списка откликов
    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.kwargs['pk']
        # print(f'id объявления: {post_id}')
        # print(f'полный queryset откликов {queryset}')
        # выделяем отклики на конкретное объявление
        # и, одновременно, только принятые отклики
        queryset = queryset.filter(commentPost_id=post_id)
        # print(f'отфильтрованы отклики на данное объявление {queryset}')
        queryset = queryset.filter(status=True)
        # print(f'отфильтрованы принятые отклики {queryset}')
        # queryset = queryset.filter(status=True, commentPost_id=post_id)

        return queryset

    # Метод get_context_data позволяет изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id_ = self.kwargs['pk']
        postCommented = Post.objects.get(id=post_id_).text
        # print(f'postCommented {postCommented}')
        # Добавляем в контекст id объявления, на которое отклик и текст.
        context['post_id'] = post_id_
        context['post_commented'] = postCommented

        return context


class NewsLetterCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_newsletter')
    raise_exception = True
    form_class = NewsLetterForm
    model = NewsLetter
    template_name = 'newsletter_create.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        # переопределение метода, чтобы добавить пользователя
        newsletter = form.save(commit=False)
        newsletter.userNewsletter = self.request.user
        return super().form_valid(form)


class ConfirmationCode(PermissionRequiredMixin, UpdateView):
    # class ConfirmationCode(UpdateView):
    model = Code
    permission_required = ('news.change_post')
    raise_exception = True
    template_name = 'user_confirm_code.html'
    form_class = ConfirmationCodeForm
    success_url = '/news'

    def form_valid(self, form):
        # переопределение метода, чтобы добавить user - текущего пользователя
        code = form.save(commit=False)
        code.user = self.request.user
        return super().form_valid(form)

class HomePageView(ListView):
    model = Post
    template_name = 'home_page.html'
