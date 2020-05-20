import { Injectable } from '@angular/core';
const data = require('../../assets/database.json');

@Injectable({
  providedIn: 'root',
})
export class CaculatorSerivce {
  database = ([] = data);
  sum: number[] = [];
  y: number[] = [];
  o: number[] = [];
  RSS: number[][] = [[], [], [], [], [], [], [], [], []];
  RSSFinal: number[] = [];
  D: number[] = [];
  Dcount: number[] = [];
  DText;
  DcountText;
  S: number[] = [];
  ES = 0;
  P: number[] = [];
  Ptx = 0;
  Pty = 0;
  Pm = 0;
  sam1 = [
    '18:d0:71:c5:86:13',
    '5c:1a:6f:da:33:a2',
    '5c:1a:6f:da:33:a1',
    '18:a6:f7:9a:a0:9c',
    'c0:b5:d7:5f:bd:c8',
  ];
  sam2 = [-59, -23, -30.333333333333332, -62.5, -43.5];
  constructor() {
    // this.database = data;
    for (let i = 0; i < this.database.length; i++) {
      this.Dcount.push(i);
    }
  }

  getLocation(arrayBssid: string[], arrayLevel: number[][]) {
    this.caculatorRSS(arrayBssid, arrayLevel);
    this.caculatorD(arrayBssid, this.RSSFinal);
    this.arrangeD(this.D);
    this.caculatorE();
    this.caculatorP();

    return this.P;
  }
  //   getLocation(arrayBssid: string[], RSSFinal: number[]) {
  //     console.log(this.database);
  //     this.caculatorD(arrayBssid, RSSFinal);
  //     this.arrangeD(this.D);
  //     this.caculatorE();
  //     this.caculatorP();

  //     return this.P;
  //   }
  test() {
    this.caculatorD(this.sam1, this.sam2);
    console.log('D:', this.D);
    this.arrangeD(this.D);
    this.caculatorE();
    this.caculatorP();
    console.log('[', +this.Ptx + ',' + this.Pty + ']');
    this.clearData();
  }

  caculatorRSS(arrayBssid: string[], arrayLevel: number[][]) {
    for (let i = 0; i < arrayBssid.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < arrayLevel[i].length; j++) {
        if (this.sum[i] == null) {
          this.sum[i] = arrayLevel[i][j];
        } else {
          this.sum[i] = this.sum[i] + arrayLevel[i][j];
        }
      }
      this.y[i] = this.sum[i] / arrayLevel[i].length;
    }

    for (let i = 0; i < arrayBssid.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < arrayLevel[i].length; j++) {
        if (this.o[i] == null) {
          this.o[i] =
            (arrayLevel[i][j] - this.y[i]) * (arrayLevel[i][j] - this.y[i]);
        } else {
          this.o[i] =
            this.o[i] +
            (arrayLevel[i][j] - this.y[i]) * (arrayLevel[i][j] - this.y[i]);
        }
      }
      this.o[i] = Math.sqrt(this.o[i] / (arrayLevel[i].length - 1));
    }

    for (let i = 0; i < arrayBssid.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < arrayLevel[i].length; j++) {
        if (
          arrayLevel[i][j] > this.y[i] - this.o[i] &&
          arrayLevel[i][j] < this.y[i] + this.o[i]
        ) {
          if (this.RSS[i][0] == null) {
            this.RSS[i][0] = arrayLevel[i][j];
          } else {
            let check = false;
            // tslint:disable-next-line:prefer-for-of
            for (let k = 0; k < this.RSS[i].length; k++) {
              if (this.RSS[i][k] === arrayLevel[i][j]) {
                check = true;
                break;
              }
            }
            if (check === false) {
              this.RSS[i].push(arrayLevel[i][j]);
            }
          }
        }
      }
    }

    for (let i = 0; i < this.RSS.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < this.RSS[i].length; j++) {
        if (this.RSSFinal[i] == null) {
          this.RSSFinal[i] = this.RSS[i][j];
        } else {
          this.RSSFinal[i] = this.RSSFinal[i] + this.RSS[i][j];
        }
      }
      this.RSSFinal[i] = this.RSSFinal[i] / this.RSS[i].length;
    }

    for (let i = 0; i < arrayBssid.length; i++) {
      if (this.o[i] === 0) {
        this.RSSFinal[i] = arrayLevel[i][0];
      }
      if (arrayLevel[i].length === 1) {
        this.RSSFinal[i] = arrayLevel[i][0];
      }
    }
    return this.RSSFinal;
  }

  clearData() {
    this.sum = [];
    this.y = [];
    this.o = [];
    this.RSS = [[], [], [], [], [], [], [], [], [], []];
    this.RSSFinal = [];
    this.D = [];
    this.Dcount = [];

    this.S = [];
    this.ES = 0;
    this.P = [];
    this.Ptx = 0;
    this.Pty = 0;
    this.Pm = 0;
    for (let i = 0; i < this.database.length; i++) {
      this.Dcount.push(i);
    }
    console.log('CLEAR DONE');
  }

  caculatorD(arrayBssid: string[], RSSFinal: number[]) {
    // tslint:disable-next-line:prefer-for-of
    for (let i = 0; i < this.database.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < arrayBssid.length; j++) {
        // tslint:disable-next-line:prefer-for-of
        for (let k = 0; k < this.database[i].bssid.length; k++) {
          if (!this.database[i].bssid[k].localeCompare(arrayBssid[j])) {
            if (this.D[i] == null) {
              this.D[i] = Math.abs(RSSFinal[j] - this.database[i].level[k]);
            } else {
              this.D[i] =
                this.D[i] + Math.abs(RSSFinal[j] - this.database[i].level[k]);
            }
          }
        }
      }
    }
  }

  arrangeD(D: number[]) {
    for (let i = 0; i < D.length - 1; i++) {
      for (let j = i + 1; j < D.length; j++) {
        if (D[i] > D[j]) {
          this.DText = D[i];
          D[i] = D[j];
          D[j] = this.DText;
          this.DcountText = this.Dcount[i];
          this.Dcount[i] = this.Dcount[j];
          this.Dcount[j] = this.DcountText;
        }
      }
    }
  }

  caculatorE() {
    for (let i = 1; i < this.D.length; i++) {
      this.S.push(this.D[0] - this.D[i]);
      this.ES = this.ES + this.S[i - 1];
    }
    this.ES = this.ES / (this.D.length - 1);
  }

  caculatorP() {
    // tslint:disable-next-line:prefer-for-of

    for (let i = 0; i < this.S.length; i++) {
      if (this.S[i] >= this.ES) {
        this.Ptx =
          this.Ptx +
          (1 / this.D[i]) *
            parseFloat(this.database[this.Dcount[i]].location[0]);

        this.Pty =
          this.Pty +
          (1 / this.D[i]) *
            parseFloat(this.database[this.Dcount[i]].location[1]);

        this.Pm = this.Pm + 1 / this.D[i];
      }
    }

    this.P.push(this.Ptx / this.Pm);
    this.P.push(this.Pty / this.Pm);
    this.Ptx = this.Ptx / this.Pm;
    this.Pty = this.Pty / this.Pm;
  }

  getRPfromDatabase() {
    return this.database;
  }
}
