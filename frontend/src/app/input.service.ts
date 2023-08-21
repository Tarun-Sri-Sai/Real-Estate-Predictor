import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class InputService {
  constructor(private http: HttpClient) {}

  makeRequest(inputData: {
    [column: string]: any;
  }): Observable<{ [key: string]: { [column: string]: any[] } }> {
    return this.http.post<any>(
      'http://localhost:5000/real_estate_predictor/input',
      inputData
    );
  }
}
