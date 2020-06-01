import { Injectable } from '@angular/core';
const data = require('../../assets/sampleESP_4.json');
const data1 = require('../../assets/sampleESP_4_v1.json');
@Injectable({
  providedIn: 'root',
})
export class TrilaSerivce {
  database = ([] = data);
  database1 = ([] = data1);
  constructor() {}
  d = 0;
  RSS = 0;
  nTu = 0;
  nMau = 0;

  location: string[] = [];
  rss: number[][] = [[], [], [], [], [], [], [], [], [], []];
  RSSnew: number[] = [
    63.625,
    80.66,
    70.46875,
    73.29,
    69.166,
    78.5,
    79.83,
    76.83,
    78,
  ];
  countLevel = 0;
  sample() {
    for (let i = 0; i < this.database1.length; i++) {
      if (i === 0) {
        this.location.push(this.database1[i].distance);
        this.rss[this.countLevel].push(this.database1[i].level[0]);
        this.countLevel++;
      } else {
        let locationCurrent = this.location.length;
        let check = true;
        for (let j = 0; j < locationCurrent; j++) {
          if (!this.database1[i].distance.localeCompare(this.location[j])) {
            this.rss[j].push(this.database1[i].level[0]);
            check = false;
            break;
          }
        }
        if (check === true) {
          let k = this.location.length;
          this.location.push(this.database1[i].distance);
          this.rss[k].push(this.database1[i].level[0]);
        }
      }
    }

    console.log(this.location);
    console.log(this.rss);

    // tslint:disable-next-line:prefer-for-of
    for (let i = 0; i < this.location.length; i++) {
      this.d = this.d + parseFloat(this.location[i]) * 0.4;
      this.RSS = this.RSS + this.RSSnew[i];
    }
    this.d = this.d / this.location.length;
    this.RSS = this.RSS / this.location.length;
    console.log(this.d + '__' + this.RSS);

    for (let i = 0; i < this.location.length; i++) {
      this.nTu =
        this.nTu +
        (parseFloat(this.location[i]) * 0.4 - this.d) * this.RSSnew[i];
      this.nMau =
        this.nMau +
        (parseFloat(this.location[i]) * 0.4 - this.d) *
          (parseFloat(this.location[i]) * 0.4 - this.d);
      console.log(
        i +
          '  ' +
          (parseFloat(this.location[i]) * 0.4 - this.d) * this.RSSnew[i] +
          '  ' +
          (parseFloat(this.location[i]) * 0.4 - this.d) *
            (parseFloat(this.location[i]) * 0.4 - this.d)
      );
    }
    console.log('n= ', this.nTu / this.nMau);
    console.log('A= ', this.RSS - (this.nTu / this.nMau) * this.d);
  }

  caculator() {
    // tslint:disable-next-line:prefer-for-of
    for (let i = 0; i < this.database.length; i++) {
      this.d = this.d + this.database[i].distance * 0.4;
      this.RSS = this.RSS + this.database[i].level[0];
    }
    this.d = this.d / this.database.length;
    this.RSS = this.RSS / this.database.length;
    console.log(this.d + '__' + this.RSS);
    // tslint:disable-next-line:prefer-for-of
    for (let i = 0; i < this.database.length; i++) {
      this.nTu =
        this.nTu +
        (this.database[i].distance * 0.4 - this.d) * this.database[i].level[0];
      this.nMau =
        this.nMau +
        (this.database[i].distance * 0.4 - this.d) *
          (this.database[i].distance * 0.4 - this.d);
      console.log(
        i +
          '  ' +
          (this.database[i].distance * 0.4 - this.d) *
            this.database[i].level[0] +
          '  ' +
          (this.database[i].distance * 0.4 - this.d) *
            (this.database[i].distance * 0.4 - this.d)
      );
    }
    console.log('n= ', this.nTu / this.nMau);
    console.log('A= ', this.RSS - (this.nTu / this.nMau) * this.d);
  }
}
