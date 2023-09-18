from django.shortcuts import render

data_modeling = {
    'modeling': [
        {
            'id': 0,
            'type': '"Букет дня"',
            'description': 'Подарите себе и своим близким мгновение яркости и радости с нашей услугой "Букет дня". Каждый день наши флористы тщательно отбирают свежие и красочные цветы, чтобы создать уникальный букет. Вы можете заказать его по специальной цене и подарить себе или кому-то другому удивительное цветочное настроение.',
            'image_url': '../static/images/bouquet_of_the_day.webp',
            'price': '5000'
            
        },
        {
            'id': 1,
            'type': 'Подарочные корзины с цветами',
            'description': 'Наши подарочные корзины - это полный праздник в одной упаковке. Мы предлагаем широкий выбор букетов цветов, которые можно дополнить шоколадом, вином, ароматическими свечами или даже плюшевыми мишками. Отправьте этот прекрасный подарок с доставкой к двери, чтобы порадовать кого-то особенного.',
            'image_url': '../static/images/basket_with_flowers.jpeg',
            'price': '7000'
        },
        {
            'id': 2,
            'type': 'Цветы на юбилей',
            'description': 'Когда наступает время отмечать важный юбилей, наши цветы делают это еще более особенным. Наши флористы создадут букет, который отражает длительность и красоту ваших отношений. Доставьте этот букет цветов с душой и стилем.',
            'image_url': '../static/images/flowers_for_anniversary.png',
            'price': '9000'
        },
        {
            'id': 3,
            'type': 'Цветы на свадьбу',
            'description': 'Для вашего особенного дня мы предлагаем услугу оформления свадебных цветов с доставкой и установкой на месте. Мы создадим магические цветочные композиции, которые подчеркнут красоту и романтику вашей свадьбы. Доверьтесь нам, чтобы сделать этот день незабываемым.',
            'image_url': '../static/images/flowers_for_merry.jpg',
            'price': '10000'
        },
        {
            'id': 4,
            'type': 'Цветы на выпускной',
            'description': 'Поздравьте выпускников с нашими уникальными букетами. Наши цветы помогут создать незабываемую атмосферу и добавят радости в это важное событие. Закажите доставку к двери и сделайте этот день особенным для них.',
            'image_url': '../static/images/flowers_for_outlet.jpg',
            'price': '8000'
        },
        {
            'id': 5,
            'type': 'Сладкий букет',
            'description': 'Мы создаем уникальные композиции, объединяя свежие цветы и вкусные сладости, чтобы сделать ваш подарок особенным. Сладкие букеты идеально подходят для различных событий - от дней рождения до свадеб и корпоративных мероприятий.',
            'image_url': '../static/images/sweet_bouquet.jpg',
            'price': '6000'
        }
    ]
}

def services(request):
    query = request.GET.get('q')

    if query:
        # Фильтруем данные, учитывая как поле "type", так и поле "price"
        filtered_data = [item for item in data_modeling['modeling'] if
                         query.lower() in item['type'].lower() or query.lower() in item['price'].lower()]

    else:
        filtered_data = data_modeling['modeling']
        query = ""

    return render(request, "pages/services.html", {'filtered_data': filtered_data, 'search_value': query})



def view_service(request, model_id):
    data_by_id = data_modeling.get('modeling')[model_id]
    return render(request, 'pages/view_service.html', {
        'modeling': data_by_id
    })
