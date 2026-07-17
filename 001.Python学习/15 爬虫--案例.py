import requests
from lxml import html
import csv
import re

target_url = 'https://www.themoviedb.org'
target_url_top = 'https://www.themoviedb.org/movie/top-rated'


def get_movie_detail(url: str):
    responses = requests.get(url)
    movie_data = html.fromstring(responses.text)
    movie_name = movie_data.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
    movie_time = movie_data.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/span/text()')
    movie_new_time = movie_data.xpath(
        '//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="release"]/text()')
    movie_type = movie_data.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]/a/text()')
    movie_runtime = movie_data.xpath(
        '//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
    movie_user_score_chart = movie_data.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')
    movie_languages = movie_data.xpath(
        '//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')
    movie_directors = movie_data.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()')
    movie_authors = movie_data.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()')
    movie_slogans = movie_data.xpath('//*[@id="original_header"]/div[2]/section/div[3]/h3[1]/text()')
    movie_description = movie_data.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')

    runtime = ''
    if movie_runtime:
        time = re.findall(r"\d+", movie_runtime[0].strip())
        runtime = int(time[0]) * 60 + int(time[1])
    else:
        runtime = ''

    movie_info = {
        '电影名': movie_name[0].strip() if movie_name else '',
        '年份': re.search(r"\d{4}", movie_time[0].strip()).group() if movie_time else '',
        '上映时间': re.match(r"\d{2}.\d{2}.\d{4}", movie_new_time[0].strip()).group() if movie_new_time else '',
        '类型': movie_type[0].strip() if movie_type else '',
        "时长": runtime,
        '评分': movie_user_score_chart[0].strip() if movie_user_score_chart else '',
        "语言": movie_languages[0].strip() if movie_languages else '',
        "导演": ','.join(movie_authors) if movie_authors else '',
        "作者": ','.join(movie_directors) if movie_directors else '',
        "宣传语": movie_slogans[0].strip() if movie_slogans else '',
        "简介": movie_description[0].strip() if movie_description else '',
    }
    return movie_info


all_movies = []


def get_data():
    data = requests.get(target_url_top)
    document = html.fromstring(data.text)
    table_list = document.xpath('//*[@class="media-list-results contents"]/div')
    for table in table_list:
        tb = table.xpath('./div/div/a/@href')
        if tb:
            movie_link = target_url + tb[0]
            movie_info = get_movie_detail(movie_link)
            all_movies.append(movie_info)
    save_data(all_movies)


def save_data(all_movies: list[dict[str, str]]) -> None:
    with open('./csv_data/02.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, all_movies[0].keys())
        writer.writeheader()
        for movie in all_movies:
            writer.writerow(movie)


if __name__ == '__main__':
    get_data()
