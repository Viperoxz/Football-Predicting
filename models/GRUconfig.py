class GRUconfig:
    def __init__(self,
                input_size = 50,
                hidden_size = 512,
                num_layer = 3,
                drop_out_rate = 0.3):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.drop_out_rate = drop_out_rate
        self.num_layer = num_layer