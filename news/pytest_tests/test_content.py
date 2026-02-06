from news.forms import CommentForm


def test_pagination(client, many_news, url_paths):
    """Тестирование пагинации."""
    response = client.get(url_paths['home'])
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    assert object_list.count() <= 10


def test_sorting_news(client, many_news, url_paths):
    """Сортировка новостей от новой к старой."""
    response = client.get(url_paths['home'])
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_sorting_comments(client, url_paths, news, many_comments):
    """Сортировка комментариев от старого к новому."""
    response = client.get(url_paths['detail'])
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_create_comment_form(client, auth_user_client, news, url_paths):
    """Проверка наличия формы создания комментария."""
    url = url_paths['detail']
    response = auth_user_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
    response = client.get(url)
    assert 'form' not in response.context
