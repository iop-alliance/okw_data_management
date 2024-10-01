from marshmallow import Schema, fields, post_load, validate, EXCLUDE
import uuid


class GeocodingSchema(Schema):

    geocoding_id = fields.Str(load_only=True)
    format = fields.Str(default='EPSG:4326')
    latitude = fields.Float(default=None)
    longitude = fields.Float(default=None)
    altitude = fields.Float(default=None)
    precision = fields.Float(default=None)

    # other_format = fields.Str()
    # other_value = fields.Str()

    @post_load
    def add_id(self, data, **kwargs):
        # Add a unique ID to the data
        data['geocoding_id'] = str(uuid.uuid4())
        # print('diag geo data:', data)
        return data


class AddressSchema(Schema):

    address_id = fields.Str(load_only=True)
    zip_code = fields.Str(default=None)
    street = fields.Str(default=None)
    number = fields.Str(default=None)
    extended = fields.Str(default=None)

    @post_load
    def add_id(self, data, **kwargs):
        # Add a unique ID to the data
        data['address_id'] = str(uuid.uuid4())
        # print('diag addr data:', data)
        return data


class RegionSchema(Schema):

    region_id = fields.Str(load_only=True)
    country = fields.Str(allow_none=True, default=None, encode_utf8=True)
    state_region = fields.Str(allow_none=True, default=None, encode_utf8=True)
    city_town = fields.Str(allow_none=True, default=None, encode_utf8=True)

    @post_load
    def add_id(self, data, **kwargs):
        # Add a unique ID to the data
        data['region_id'] = str(uuid.uuid4())
        # print('diag reg data:', data)
        return data


class LocationSchema(Schema):

    location_id = fields.Str(load_only=True)
    geocoding_id = fields.Str(allow_none=True, default=None)
    address_id = fields.Str(allow_none=True, default=None)
    region_id = fields.Str(allow_none=True, default=None)

    @post_load
    def add_id(self, data, **kwargs):
        # Add a unique ID to the data
        data['location_id'] = str(uuid.uuid4())
        # print('diag loc data:', data)
        return data


class FacilitySchema(Schema):

    facility_id = fields.Str(load_only=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)
    description = fields.Str(required=True)
    inventory = fields.Str(default=None)
    location_id = fields.Str(required=True)

    @post_load
    def add_id(self, data, **kwargs):
        # Add a unique ID to the data
        data['facility_id'] = str(uuid.uuid4())
        # print('diag fac data:', data)
        return data


class ParserSchema:
    def set_geocoding_schema(self, values):
        # print('diag values geo:', values)
        __schema = GeocodingSchema()

        try:
            __out = __schema.load(values,
                                  # many=False,
                                  partial=True,
                                  unknown=EXCLUDE
                                  )
            self.geocoding = __out
            # # print('geocod type:', self.geocoding)
            # print('geocod type:', __out)


            return True

        except Exception as ex:
            # print('err geocoding', ex)
            self.geocoding = None
            return False

    def set_address_schema(self, values):
        try:
            __schema = AddressSchema()
            __out = __schema.load(values, many=False, partial=True, unknown=EXCLUDE)
            self.address = __out
            # print(self.address)
            return True
        except Exception as ex:
            self.address = None
            # print(ex, 'err address')
            return False

    def set_region_schema(self, values):
        try:
            __schema = RegionSchema()
            __out = __schema.load(values, many=False, partial=True, unknown=EXCLUDE)
            self.region = __out
            # print(self.region)
            return True
        except Exception as ex:
            self.region = None
            # print(ex, 'err region')
            return False

    def set_location_schema(self):
        __schema = LocationSchema()

        try:
            # print('diag set loc sch type:', self.geocoding)
            __geocoding_id = self.geocoding['geocoding_id']
        except TypeError:
            __geocoding_id = None

        try:
            __address_id = self.address['address_id']
        except TypeError:
            __address_id = None

        try:
            __region_id = self.region['region_id']
        except TypeError:
            __region_id = None

        __in = {'geocoding_id': __geocoding_id, 'address_id': __address_id,
                'region_id': __region_id}
        # print('diag set loc')
        # print(__in)

        __out = __schema.load(__in)
        # print(__out)
        self.location = __out
        return True
        # except Exception as ex:
        #    # print(ex, 'err loc')
        #    return False

    def set_facility_schema(self, values):
        # try:
        __schema = FacilitySchema()
        __out = __schema.load(values, many=False, partial=True, unknown=EXCLUDE)
        self.facility = __out
        # not sure
        # print('diag set fac id')
        self.facility['location_id'] = self.location['location_id']
        return True

        # except Exception as ex:
        #    # print(ex, 'err fa')
        #    return False

    def dumping(self, values):
        if not isinstance(values, dict):
            # print('err dumping')
            return False
        else:
            self.set_geocoding_schema(values)
            self.set_address_schema(values)
            self.set_region_schema(values)
            self.set_location_schema()
            self.set_facility_schema(values)

            return {'geocoding': self.geocoding,
                    'address': self.address,
                    'region': self.region,
                    'location': self.location,
                    'facility': self.facility}
