from datetime import datetime

now = datetime.now()


def req_data(url):
    response = requests.get(url)

    print(response.status_code)

    if response.status_code == 200:
        return response
    else:
        print("Error response: Check URL or internet avalability, and Try again.")
        print(url)


url = "https://makery.gogocarto.fr/api/elements.json"
data = req_data(url).json()
print(type(data))

data_ = pd.DataFrame(data)

input_d = pd.DataFrame(data_.data)
print(input_d.shape)

from pandas import json_normalize

input_ = pd.json_normalize(input_d['data'])

input_.reset_index(drop=True, inplace=True)

input_.to_csv('../data/raw_makery_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')

input_.columns.tolist()

transform = input_.rename(
    columns={'id': 'makery_id', 'status': 'makery_status', 'site_web': 'url', 'geo.latitude': 'latitude',
             'geo.longitude': 'longitude'})

# transform['makery_url'] = 'https://makery.gogocarto.fr/map#/fiche/{name}/{id}/'.format(name=transform.name.replace(' ','-'), id=transform.makery_id)

transform['makery_url'] = transform.apply(
    lambda row: 'https://makery.gogocarto.fr/map#/fiche/{name}/{id}/'.format(
        name=str(row['name']).replace(' ', '-'),
        id=row['makery_id']
    ),
    axis=1
)

transform = transform[transform['makery_status'] != 'closed']

transform = transform[transform['makery_status'] != 'planned']

transform['address_composed'] = transform['address.streetNumber'].astype(str) + ', ' + transform[
    'address.streetAddress'].astype(str) + ', ' + transform['address.addressLocality'].astype(str) + ', ' + transform[
                                    'address.postalCode'].astype(str) + ', ' + transform[
                                    'address.addressCountry'].astype(str)

drops = [
    'sourceKey',
    'categoriesFull',
    'article_makery',
    'fullAddress',
    'mode_gestion',
    'subscriberEmails',
    'address.customFormatedAddress',
    'description_courte',
    'surface',
    'telephone',
    'images',
    'openHours.Mo',
    'openHours.Tu',
    'openHours.We',
    'openHours.Th',
    'openHours.Fr',
    'address.streetNumber',
    'address.streetAddress',
    'address.addressLocality',
    'address.postalCode',
    'address.addressCountry',
    'affiliation',
    'description',
    'openHours.Sa',
    'openHours.Su']

output = transform.drop(columns=drops)

output.columns.tolist()

output.to_csv('../data/iopa_makery_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')

print("OKW entries: {r[0]}, columns = {r[1]}".format(r=output.shape))