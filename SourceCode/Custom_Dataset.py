from torch.utils.data.dataset import Dataset


class Custom_Dataset(Dataset):
    def __init__(self, ...):

    # stuff

    def __getitem__(self, index):
        # stuff
        return (img, label)

    def __len__(self):
        return count  # of how many examples(images?) you have