import { Component } from '@angular/core';
import { ColumnsService } from './columns.service';
import { DataValuesService } from './data-values.service';
import { PriceService } from './price.service';

@Component({
  selector: 'app-input',
  template: `
    <h6 *ngFor="let column of columnsService.getColumns()">
      <div class="label">
        <label [for]="column">
          {{ transformColumnName(column) + ":" }}
        </label>
      </div>
      <div *ngIf="isEncoded(column)">
        <ng-select
          class="form-select top-spacing"
          [id]="column"
          [(ngModel)]="selectedOption[column]"
          [items]="dataValuesService.getDataValues()[column]"
          bindLabel="item"
          bindValue="item"
          [searchFn]="customSearch"
          (change)="sendInput()"
        >
          <ng-template ng-option-tmp let-item="item">{{ item }}</ng-template>
        </ng-select>
      </div>
      <div *ngIf="!isEncoded(column)">
        <input
          class="input top-spacing"
          type="text"
          [(ngModel)]="selectedOption[column]"
          (change)="sendInput()"
        />
      </div>
    </h6>

  `,
  styles: [`
    .form-select ::ng-deep .ng-dropdown-panel {
      border: 1px solid rgba(0, 0, 0, 0.25);
      border-radius: 5px;
      background-color: #ffffff;
      margin-left: -12px;
    }

    .form-select ::ng-deep .ng-dropdown-panel .ng-option {
      padding: 8px;
    }

    .input {
      border: 1px solid rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      padding: 8px;
      width: 100%;
    }

  `],
})
export class InputComponent {
  inputData: { [column: string]: any } = {};
  selectedOption: { [column: string]: any } = {};

  constructor(
    public columnsService: ColumnsService,
    public dataValuesService: DataValuesService,
    private priceService: PriceService
  ) {}

  transformColumnName(column: string): string {
    return column
      .split('_')
      .map((word) => {
        if (word.includes('/')) {
          return word.toUpperCase();
        }
        return word.charAt(0).toUpperCase() + word.slice(1);
      })
      .join(' ');
  }

  sendInput(): void {
    this.getInputData();
    for (let column of this.columnsService.getColumns()) {
      if (!this.inputData[column]) {
        return;
      }
    }
    this.priceService.predictPrice(this.inputData);
  }

  getInputData(): void {
    for (let column of this.columnsService.getColumns()) {
      this.inputData[column] = this.selectedOption[column];
    }
  }

  customSearch(term: string, item: any): boolean {
    return item.toString().toLowerCase().includes(term.toLowerCase());
  }

  isEncoded(column: string): boolean {
    return this.dataValuesService.getDataValues().hasOwnProperty(column);
  }
}

