from collections import Counter
from itertools import groupby


def main():
    # 1
    moscow = {201, 202, 203, 204}
    kazan = {203, 204, 205, 206}

    both_cities = moscow.intersection(kazan)
    only_moscow = moscow.difference(kazan)
    only_kazan = kazan.difference(moscow)
    uniq_in_both_cities = len(moscow | kazan)

    print(
        'Задание 1\n',
        f'Можно забрать в любом из двух городов: {both_cities}\n',
        f'Только в Москве: {only_moscow}\n',
        f'Только в Казани: {only_kazan}\n',
        f'Число всех уникальных товаров: {uniq_in_both_cities}',
    )

    # 2
    queries = [
        'чехол',
        'iphone',
        'чехол',
        'наушники',
        'iphone',
        'iphone',
        'кабель',
        'чехол',
        'iphone',
    ]

    count_queries = len(queries)
    count_type_query = Counter(queries)
    most_common_query, most_common_count = (
        count_type_query.most_common(1)[0][0],
        count_type_query.most_common(1)[0][1],
    )
    ratio_most_common = most_common_count / count_queries
    rare_query = {key for key, value in count_type_query.items() if value == 1}

    print(
        'Задание 2' + '\n',
        f'Всего поисковых запросов в ленте: {count_queries}' + '\n',
        f'Каждый запрос ввели: {dict(count_type_query)}' + '\n',
        f'Вводили чаще всего: {most_common_query}' + '\n',
        'Доля самого частого запроса среди остальных: '
        f'{ratio_most_common}' + '\n',
        f'Встетились один раз: {rare_query}',
    )

    # 3
    orders = [
        {'id': 1, 'buyer': 'anya', 'status': 'delivered', 'amount': 900},
        {'id': 2, 'buyer': 'boris', 'status': 'returned', 'amount': 4_500},
        {'id': 3, 'buyer': 'anya', 'status': 'delivered', 'amount': 1_500},
        {'id': 4, 'buyer': 'vera', 'status': 'delivered', 'amount': 3_200},
        {'id': 5, 'buyer': 'boris', 'status': 'delivered', 'amount': 700},
        {'id': 6, 'buyer': 'gleb', 'status': 'returned', 'amount': 2_100},
    ]

    print('Задание 3')
    returned_sum = sum(
        [item['amount'] for item in orders if item['status'] == 'returned']
    )
    print(f'Сумма возвратов: {returned_sum}')

    buyers_returned_once = {
        item['buyer'] for item in orders if item['status'] == 'returned'
    }
    print(
        'Покупатели, которые вернули товар хотя бы один раз: '
        f'{buyers_returned_once}'
    )

    sorted_delivered = groupby(
        sorted(orders, key=lambda order: order['buyer']),
        key=lambda order: order['buyer'],
    )
    print('Доставленных заказов на человека:')
    for group, value in sorted_delivered:
        delivered_orders = [
            item['id'] for item in value if item['status'] == 'delivered'
        ]
        print(f'{group} : {len(delivered_orders)}')

    delivered_amount = [
        item['amount'] for item in orders if item['status'] == 'delivered'
    ]
    average_amount = sum(delivered_amount) / len(delivered_amount)
    print(f'Средний чек доставленных заказов: {average_amount}')

    # 4
    days = [
        {'day': 'пн', 'orders': 20, 'revenue': 40_000, 'returns': 2},
        {'day': 'вт', 'orders': 16, 'revenue': 19_200, 'returns': 4},
        {'day': 'ср', 'orders': 25, 'revenue': 55_000, 'returns': 1},
        {'day': 'чт', 'orders': 10, 'revenue': 12_000, 'returns': 3},
        {'day': 'пт', 'orders': 30, 'revenue': 48_000, 'returns': 3},
    ]

    print('Задание 4')

    sum_amount = sum([item['revenue'] for item in days])
    print(f'Выручка за всю неделю: {sum_amount}')

    day_max_revenue = [
        item['day']
        for item in sorted(days, key=lambda x: x['revenue'], reverse=True)
    ][:1]
    print(f'День с максимальной выручкой: {day_max_revenue}')

    average_days_amount = {
        item['day']: item['revenue'] / item['orders'] for item in days
    }
    print(f'Средняя выручка на один заказ по дням: {average_days_amount}')

    more_than_20 = [
        item['day']
        for item in days
        if (item['returns'] / item['orders']) > 0.2
    ]
    print(f'Дни с долей возвратов более 20%: {more_than_20}')

    # 5
    reviews = [
        {'id': 1, 'product': 'Чехол', 'stars': 5},
        {'id': 1, 'product': 'Чехол', 'stars': 3},
        {'id': 1, 'product': 'Чехол', 'stars': 4},
        {'id': 2, 'product': 'Наушники', 'stars': 2},
        {'id': 2, 'product': 'наушники', 'stars': 2},
        {'id': 2, 'product': 'НАУШНИКИ', 'stars': 5},
        {'id': 3, 'product': 'Планшет', 'stars': 5},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 5, 'product': 'Кабель', 'stars': 1},
    ]

    print('Задание 5')

    sorted_group = groupby(
        sorted(reviews, key=lambda x: x['product'].lower()),
        key=lambda x: x['product'].lower(),
    )
    average_rates = []
    print('Средняя оценка каждого товара: ')
    for group, value in sorted_group:
        value = list(value)
        average_rate = sum([item['stars'] for item in value]) / len(value)
        print(f'{group}: {average_rate}')
        if len(value) >= 2:
            average_rates.append((group, average_rate))
    worst_product = [
        item[0]
        for item in sorted(average_rates, key=lambda x: x[1])
    ][:1]
    print(
        'Худший товар по средней оценке среди тех, у кого хотя бы два '
        'отзыва: '
        f'{worst_product}'
    )

    low_stars = Counter(
        item['stars'] for item in reviews if item['stars'] in (1, 2)
    )
    sum_low_stars = sum(v for _, v in low_stars.items())
    print(f'Отзывов на 1 или 2 звезды: {sum_low_stars}')

    ratio_stars = sum_low_stars / sum(
        v for _, v in Counter(item['stars'] for item in reviews).items()
    )
    print(f'Какую долю всех отзывов они составляют: {ratio_stars}')


if __name__ == '__main__':
    main()
