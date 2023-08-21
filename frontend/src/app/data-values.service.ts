import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class DataValuesService {
  private dataValues: { [column: string]: any[] } = {};

  constructor(private http: HttpClient) {
    this.makeRequest();
  }

  makeRequest(): void {
    this.http
      .get<any>('http://localhost:5000/real_estate_predictor/data_values')
      .subscribe({
        next: (response) => {
          this.dataValues = response['data_values'];
        },
        error: (err) => {
          console.error('Unable to receive data values due to ', err);
        },
      });
  }

  getDataValues(): { [column: string]: any[] } {
    return this.dataValues;
  }
}
