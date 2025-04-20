import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class PriceService {
  price: number = 0;

  constructor(private http: HttpClient) {}

  predictPrice(inputData: { [column: string]: any }): void {
    let params = new HttpParams();
    for (const key in inputData) {
        params = params.append(key, JSON.stringify(inputData[key]));
    }

    this.http
      .get<any>('http://localhost/api/prediction', {
        params
      })
      .subscribe({
        next: (response) => {
          this.price = response['price_in_lacs'];
        },
        error: (error) => {
          console.log("Couldn't predict price due to ", error);
        },
      });
  }

  getPrice(): number {
    return this.price;
  }
}
