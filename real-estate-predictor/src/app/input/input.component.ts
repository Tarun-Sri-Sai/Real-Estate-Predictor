import { Component, OnInit } from '@angular/core'
import { AppService } from '../app.service'
import { HttpClient } from '@angular/common/http'

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent implements OnInit {
  columns: string[] = []
  dataValues: { [column: string]: any[] } = {}
  inputData: { [column: string]: any } = {}
  processedInput: { [column: string]: any[] } = {}
  selectedOption: { [column: string]: any } = {}

  constructor(private http: HttpClient, public app: AppService) { }

  ngOnInit() {
    this.getColumns()
    this.getDataValues()
  }

  getColumns(): void {
    this.http.get<any>('http://localhost:5000/get_column_names')
      .subscribe({
        next: (response) => {
          this.columns = response['column_names']
        },
        error: (err) => {
          console.error('Unable to receive columns due to ', err)
        }
      })
  }

  getDataValues(): void {
    this.http.get<any>('http://localhost:5000/get_data_values')
      .subscribe({
        next: (response) => {
          this.dataValues = response['data_values']
        },
        error: (err) => {
          console.error('Unable to receive data values due to ', err)
        }
      })
  }

  transformColumnName(column: string): string {
    return column.split('_').map((word) => {
      if (word.includes('/')) {
        return word.toUpperCase()
      }
      return word.charAt(0).toUpperCase() + word.slice(1)
    }).join(' ')
  }

  getResult(): void {
    this.getInputData()

    for (let column of this.columns) {
        if (!this.inputData[column]) {
        return
      }
    }

    this.http.post<any>('http://localhost:5000/process_input', this.inputData)
      .subscribe({
        next: (response) => {
          this.processedInput = response['processed_input']
          this.http.post<any>('http://localhost:5000/get_pred', this.processedInput)
            .subscribe({
              next: (response) => {
                this.app.result = response['price_in_lacs']
              },
              error: (err) => {
                console.error('Unable to get price due to ', err)
              }
            })
        },
        error: (err) => {
          console.error('Unable to process input data due to ', err)
        }
      })
  }

  getInputData(): void {
    for (let column of this.columns) {
      this.inputData[column] = this.selectedOption[column]
    }
  }

  customSearch(term: string, item: any): boolean {
    return item.toString().toLowerCase().includes(term.toLowerCase())
  }
}
