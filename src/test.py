from app import App
import random as rn


def main():
    app = App()

    data_values = app.get_data_values()
    input_dict = dict((column, rn.choice(data_values[column])) 
                      for column in app.get_columns())

    print(input_dict)

    processed = app.process_input(input_dict)
    print(app.get_pred(processed))


if __name__ == "__main__":
    main()
