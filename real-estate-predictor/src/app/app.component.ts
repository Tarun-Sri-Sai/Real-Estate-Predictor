import { Component, OnInit } from '@angular/core'
import { HttpClient } from '@angular/common/http'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  columns: string[] = []
  dataValues: { [column: string]: any } = {}

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getColumns()
    this.getDataValues()
  }

  getColumns(): void {
    this.http.get<any>('http://localhost:5000/get_column_names')
      .subscribe({
        next: (response) => {
          this.columns = response['column_names']
          console.log(this.columns)
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
          console.log(this.dataValues)
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
}