import sense_hat

sense = sense_hat.SenseHat()

temperature = int(round(sense.get_temperature()))

sense.show_message("{} C".format(temperature), text_colour = [255, 0, 0])

