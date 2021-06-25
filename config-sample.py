import domain

import os


DAYS_ADVANCE = 14
LEISURE_CENTRES = [
    domain.LeisureCentre(122, 'The Triangle, Burgess Hill', [
        domain.Location('8ecba194-543b-4235-824d-746e2f0e9fdf', 'Main Pool'),
        domain.Location('313bef82-8f3d-4707-bfef-d44d34480181', 'Leisure Pool'),
        domain.Location('22dcdb49-132b-4946-8e84-8ebd44c3ca2e', 'Ourdoor Pool'),
        domain.Location('13e4f0ed-af13-4bf3-83d8-1f8985b5a029', 'Flumes'),
        domain.Location('fba3a440-d7b6-4720-98df-5a131ad8a37e', 'Lido'),
        domain.Location('89f0154c-3a7c-4e4e-b064-4ad46e194f02', 'Health Suite')
    ]),
    domain.LeisureCentre(123, 'The Dolphin, Haywards Heath', [
        domain.Location('8ecba194-543b-4235-824d-746e2f0e9fdf', 'Main Pool'),
        domain.Location('e311844f-a091-4baa-94c1-2c0a5876eb63', 'Teaching Pool'),
        domain.Location('89f0154c-3a7c-4e4e-b064-4ad46e194f02', 'Health Suite')
    ]),
    domain.LeisureCentre(124, 'The Kings Centre, East Grinstead', [
        domain.Location('8ecba194-543b-4235-824d-746e2f0e9fdf', 'Main Pool'),
        domain.Location('e311844f-a091-4baa-94c1-2c0a5876eb63', 'Teaching Pool')
    ]),
]
OUTPUT_DIR = os.path.join(os.pardir, 'httpdocs')
REQUEST_DELAY_SECONDS = 1
STATIC_DIR = 'static'
SWIM_TIMETABLE_ID = '1c3c1068-2173-4ae4-b7f7-fc6b55da0549'
