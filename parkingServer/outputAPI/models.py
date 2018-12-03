from mainModels.models import ArduinoOutput, Spot

# Create your models here.

class DisplayState(object):

    def __init__(self, outputID):
        YELLOW_MAX = 2


        parking_lot = ArduinoOutput.objects.get(pk=outputID).parking_lot

        self.lightState = []
        available = 0
        active = 0

        rows = parking_lot.lot_state.first().rows.order_by('pk')

        for row in rows:
            if not row.active:
                break
            active_spots = row.spots.filter(active=True)
            available_spots = active_spots.filter(full=False)
            # print("row: " + str(row.pk))
            # print("available: " + str(available_spots))
            # print("active: " + str(active_spots))

            if available_spots.count() > YELLOW_MAX:
                self.lightState.append(1)
            elif available_spots.count() > 0:
                self.lightState.append(2)
            else:
                self.lightState.append(3)

            available += available_spots.count()
            active += active_spots.count()

        additional_active_spots = Spot.objects.filter(row=None).exclude(sector_spot=None).count()


        active += additional_active_spots

        self.signState = {
            "num_available_spots": available,
            "num_active_spots": active
        }

    def get_dict(self):
        dict = {
            "lightState": self.lightState,
            "signState": self.signState
        }

        return dict



