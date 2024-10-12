import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ColumnsService {
  private columns: string[] = [];

  constructor(private http: HttpClient) {
    this.makeRequest();
  }

  makeRequest(): void {
    this.http
      .get<any>('http://localhost:5000/real_estate_predictor/column_names')
      .subscribe({
        next: (response) => {
          this.columns = response['column_names'];
        },
        error: (err) => {
          console.error('Unable to receive columns due to ', err);
        },
      });
  }

  getColumns(): string[] {
    return this.columns;
  }
}
