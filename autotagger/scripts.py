import argparse

from autotagger.stackoverflow import linear as so_linear


def linear_regression():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_name', nargs=1)
    parser.add_argument('--full-dataset', dest='use_full_dataset',
                        action='store_true')
    parser.set_defaults(use_full_dataset=False)
    args = parser.parse_args()

    dataset_name = args.dataset_name[0]
    use_full_dataset = args.use_full_dataset

    if dataset_name == 'stackoverflow':
        so_linear.linear_regression(use_full_dataset)
    else:
        pass
