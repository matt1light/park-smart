from graphene_django import DjangoObjectType
import graphene
from mainModels.models import LotState, Row, Sector, Spot, SectorSpot, ImageCoordinates

class LotStateType(DjangoObjectType):
    class Meta:
        model = LotState

class QueryLotState(graphene.ObjectType):
    all_lot_states = graphene.List(LotStateType)

    lot_state = graphene.Field(
        LotStateType,
        id=graphene.Int()
    )

    def resolve_lot_state(self, info, **args):
        id = args.get('id')
        return LotState.objects.get(pk=id)

    def resolve_all_lot_states(self, info):
        return LotState.objects.all()

class RowType(DjangoObjectType):
    class Meta:
        model = Row

class QueryRow(graphene.ObjectType):
    all_rows = graphene.List(RowType)
    row = graphene.Field(
        RowType,
        id = graphene.Int()
    )

    def resolve_all_rows(self, info):
        return Row.objects.all()

    def resolve_row(self, info, **args):
        id = args.get('id')
        return Row.objects.get(pk= id)

class SectorType(DjangoObjectType):
    class Meta:
        model = Sector

class QuerySector(graphene.ObjectType):
    sector = graphene.Field(
        SectorType,
        id=graphene.Int()
    )

    all_sectors = graphene.List(SectorType)

    def resolve_sector(self, info, **args):
        id = args.get('id')
        return Sector.objects.get(pk=id)

    def resolve_all_sectors(self, info):
        return Sector.objects.all()

class SpotType(DjangoObjectType):
    class Meta:
        model = Spot

class QuerySpot(graphene.ObjectType):
    all_spots = graphene.List(SpotType)
    spot = graphene.Field(
        SpotType,
        id = graphene.Int()
    )

    def resolve_all_spots(self, info):
        return Spot.objects.all()

    def resolve_spot(self, info, **args):
        id = args.get('id')
        return Spot.objects.get(pk= id)

class SectorSpotType(DjangoObjectType):
    class Meta:
        model = SectorSpot

class QuerySectorSpot(graphene.ObjectType):
    sector_spot = graphene.List(SectorSpotType)

    def resolve_sector_spot(self, info):
        return SectorSpot.objects.all()

class ImageCoordinatesType(DjangoObjectType):
    class Meta:
        model = ImageCoordinates

class QueryImageCoordinates(graphene.ObjectType):
    image_coordinates = graphene.List(ImageCoordinatesType)

    def resolve_image_coordinates(self, info):
        return ImageCoordinates.objects.all()

class UpdateSector(graphene.Mutation):
    id = graphene.Int(required=True)
    x_index = graphene.Int(required=True)
    y_index = graphene.Int(required=True)
    class Arguments:

        id = graphene.Int(required=True)
        x_index = graphene.Int(required=True)
        y_index = graphene.Int(required=True)

    def mutate(self, info, **args):
        id = args.get('id')
        x_index = args.get('x_index')
        y_index = args.get('y_index')

        sector = Sector.objects.get(pk=id)
        sector.x_index = x_index
        sector.y_index = y_index
        sector.save(update_fields=['x_index', 'y_index'])

        return UpdateSector(
            id=sector.pk,
            x_index=sector.x_index,
            y_index=sector.y_index
        )

class MutationSector(graphene.ObjectType):
    update_sector = UpdateSector.Field()

class Mutation(MutationSector):
    pass

class Query(QueryLotState, QueryRow, QuerySector, QuerySpot, QueryImageCoordinates):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
