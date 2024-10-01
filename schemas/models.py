import marimo

__generated_with = "0.7.5"
app = marimo.App(width="medium")


@app.cell
def __(post_load, uuid):
    from marshmallow import Schema, fields

    class GeocodingSchema(Schema):
        """
        Schema for geocoding data.

        Attributes:
        - gps_id: GPS identifier (str)
        - latitude: Latitude coordinate (float)
        - longitude: Longitude coordinate (float)
        - altitude: Altitude coordinate (float)
        - precision: Precision of the coordinates (float)
        - other_format: Other format for geocoding data (str)
        - other_value: Other value for geocoding data (str)

        Methods:
        - None
        """
        geocoding_id = fields.Str(dump_only=True)
        format = fields.Str(required=True)
        latitude = fields.Float()
        longitude = fields.Float()
        altitude = fields.Float()
        precision = fields.Float()
        other_format = fields.Str()
        other_value = fields.Str()

        @post_load
        def add_id(self, data, **kwargs):
            # Add a unique ID to the data
            data['geocoding_id'] = str(uuid.uuid4())
            return data



    class AddressSchema(Schema):
        """
        Schema for address data.

        Attributes:
        - address_id: Unique identifier for the address (str)
        - zip_code: Zip code or postal code (str)
        - street: Street name (str)
        - number: House number (str)
        - extended: Extended information about the address (str)

        Methods:
        - None
        """
        address_id = fields.Str(dump_only=True)
        zip_code = fields.Str()
        street = fields.Str()
        number = fields.Str()
        extended = fields.Str()

        @post_load
        def add_id(self, data, **kwargs):
            # Add a unique ID to the data
            data['address_id'] = str(uuid.uuid4())
            return data



    class RegionSchema(Schema):
        """
        Schema for region data.

        Attributes:
        - region_id: Unique identifier for the region (str)
        - country: Country name (str)
        - state_region: State or region name (str)
        - city_town: City or town name (str)

        Methods:
        - None
        """
        region_id = fields.Str(dump_only=True)
        country = fields.Str()
        state_region = fields.Str()
        city_town = fields.Str()

        @post_load
        def add_id(self, data, **kwargs):
            # Add a unique ID to the data
            data['region_id'] = str(uuid.uuid4())
            return data


    class LocationSchema(Schema):
        """
        Schema for location data.

        Attributes:
        - location_id: Unique identifier for the location (str)

        Methods:
        - None
        """
        location_id = fields.Str(dump_only=True)
        geocoding_id = fields.Str(required=True)
        address_id = fields.Str(required=True)
        region_id = fields.Str(required=True)

        @post_load
        def add_id(self, data, **kwargs):
            # Add a unique ID to the data
            data['region_id'] = str(uuid.uuid4())
            return data


    class ManufacturingFacilitySchema(Schema):
        """
        Schema for manufacturing facility data.

        Attributes:
        - facility_id: Unique identifier for the facility (int)
        - name: Name of the facility (str)
        - description: Description of the facility (str)
        - type: Type of the facility (str)
        - inventory: Inventory information about the facility (str)
        - language: Language spoken at the facility (str)

        Methods:
        - set_location(location_dict): Sets the location for the facility
        """


        facility_id = fields.Str(dump_only=True)
        name = fields.Str(required=True)
        description = fields.Str(required=True)
        type = fields.Str(required=True)
        inventory = fields.Str()
        location_id = fields.Str(required=True)

        @post_load
        def add_id(self, data, **kwargs):
            # Add a unique ID to the data
            data['facility_id'] = str(uuid.uuid4())
            return data
    return (
        AddressSchema,
        GeocodingSchema,
        LocationSchema,
        ManufacturingFacilitySchema,
        RegionSchema,
        Schema,
        fields,
    )


if __name__ == "__main__":
    app.run()
