import note_seq

class ChordEncoder(note_seq.EventSequenceEncoderDecoder):
    def input_size(self):
        return 1

    def num_classes(self):
        return 1

    def default_event_label(self):
        return 1

    def events_to_input(self, events, position):
        return [0]