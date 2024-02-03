import argparse


def manage_report():
    # ...
    print('will generate report')
    # ...
    return


def manage_daily_db_update():
    # ...
    print('will update daily db')
    # ...
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', action='store_true', help='run report script')  # the `store_true` action stores `True` if the argument is present, and `False` otherwise
    parser.add_argument('--update', action='store_true', help='run update script')
    args = parser.parse_args()

    if args.report:
        manage_report()
    elif args.update:
        manage_daily_db_update()
    else:
        manage_report()
        manage_daily_db_update()
