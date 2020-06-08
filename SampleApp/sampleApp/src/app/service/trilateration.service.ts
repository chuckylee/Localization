import { Injectable } from '@angular/core';
const data = require('../../assets/dataTrila.json');
@Injectable({
  providedIn: 'root',
})
export class TrilaSerivce {
  database = ([] = data);
  distanceValue: number[] = [];
  RSS: number[][] = [[], [], [], [], [], [], [], [], []];
  RSSFinal: number[] = [];
  TriangleValue: number[] = [];
  NameTriangle: string[][] = [
    ['ESP32-1', 'ESP32-3', 'ESP32-4'],
    ['ESP32-1', 'ESP32-2', 'ESP32-4'],
  ];
  TriangleChoosen = 0;
  locationTrila: number[] = [];
  constructor() {}
  check(arrayName: string[], arrayLevel: number[][]) {
    // console.log('TriangleChoosen: ', this.TriangleChoosen);
    // console.log('name: ', arrayName);
    this.caculatorRSS(arrayName, arrayLevel);
    this.caculatorDistance(arrayName);
    // console.log('distance: ', this.distanceValue);
    this.defineTriangle(arrayName);
    // console.log('TriangleValue: ', this.TriangleValue);
    // console.log(Math.min.apply(null, this.TriangleValue));
    // console.log(
    //   'TriangleChoosen: ',
    //   this.TriangleChoosen + '  ' + this.NameTriangle[this.TriangleChoosen]
    // );
    this.defineLocation(arrayName);
    console.log(
      'Location: [' +
        this.locationTrila[0] +
        ' , ' +
        this.locationTrila[1] +
        ']'
    );
  }
  getLocation(arrayName: string[], arrayLevel: number[][]) {
    this.caculatorRSS(arrayName, arrayLevel);
    this.caculatorDistance(arrayName);
    console.log('distance: ', this.distanceValue);
    this.defineTriangle(arrayName);
    console.log('TriangleValue: ', this.TriangleValue);
    console.log(Math.min.apply(null, this.TriangleValue));
    console.log(
      'TriangleChoosen: ',
      this.TriangleChoosen + '  ' + this.NameTriangle[this.TriangleChoosen]
    );
    this.defineLocation(arrayName);
    console.log(
      'Location: [' +
        this.locationTrila[0] +
        ' , ' +
        this.locationTrila[1] +
        ']'
    );
    return this.locationTrila;
  }

  caculatorRSS(arrayName: string[], arrayLevel: number[][]) {
    let sum: number[] = [];
    let y: number[] = [];
    let o: number[] = [];
    for (let i = 0; i < arrayName.length; i++) {
      for (let j = 0; j < arrayLevel[i].length; j++) {
        if (sum[i] == null) {
          sum[i] = arrayLevel[i][j];
        } else {
          sum[i] = sum[i] + arrayLevel[i][j];
        }
      }
      y[i] = sum[i] / arrayLevel[i].length;
    }

    for (let i = 0; i < arrayName.length; i++) {
      for (let j = 0; j < arrayLevel[i].length; j++) {
        if (o[i] == null) {
          o[i] = (arrayLevel[i][j] - y[i]) * (arrayLevel[i][j] - y[i]);
        } else {
          o[i] = o[i] + (arrayLevel[i][j] - y[i]) * (arrayLevel[i][j] - y[i]);
        }
      }
      o[i] = Math.sqrt(o[i] / (arrayLevel[i].length - 1));
    }

    for (let i = 0; i < arrayName.length; i++) {
      for (let j = 0; j < arrayLevel[i].length; j++) {
        if (arrayLevel[i][j] > y[i] - o[i] && arrayLevel[i][j] < y[i] + o[i]) {
          if (this.RSS[i][0] == null) {
            this.RSS[i][0] = arrayLevel[i][j];
          } else {
            let check = false;
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
      for (let j = 0; j < this.RSS[i].length; j++) {
        if (this.RSSFinal[i] == null) {
          this.RSSFinal[i] = this.RSS[i][j];
        } else {
          this.RSSFinal[i] = this.RSSFinal[i] + this.RSS[i][j];
        }
      }
      this.RSSFinal[i] = this.RSSFinal[i] / this.RSS[i].length;
    }

    for (let i = 0; i < arrayName.length; i++) {
      if (o[i] === 0) {
        this.RSSFinal[i] = arrayLevel[i][0];
      }
      if (arrayLevel[i].length === 1) {
        this.RSSFinal[i] = arrayLevel[i][0];
      }
    }
    return this.RSSFinal;
  }
  caculatorDistance(arrayName: string[]) {
    for (let i = 0; i < arrayName.length; i++) {
      for (let j = 0; j < this.database.length; j++) {
        if (!arrayName[i].localeCompare(this.database[j].name)) {
          this.distanceValue[i] = Math.pow(
            10,
            (this.average_RSS(this.database[j].level) - this.RSSFinal[i]) / 20
          );
        }
      }
    }
  }

  average_RSS(RSS: number[]) {
    let value = 0;
    for (let i = 0; i < RSS.length; i++) {
      value = value + RSS[i];
    }
    value = value / RSS.length;
    return value;
  }

  defineTriangle(arrayName: string[]) {
    for (let i = 0; i < this.NameTriangle.length; i++) {
      for (let j = 0; j < arrayName.length; j++) {
        for (let k = 0; k < this.NameTriangle[i].length; k++) {
          if (!arrayName[j].localeCompare(this.NameTriangle[i][k])) {
            if (this.TriangleValue[i] == null) {
              this.TriangleValue.push(this.distanceValue[j]);
            } else {
              this.TriangleValue[i] =
                this.TriangleValue[i] + this.distanceValue[j];
            }

            console.log(i + ':  ' + this.distanceValue[j]);
          }
        }
      }
    }

    for (let i = 0; i < this.TriangleValue.length; i++) {
      if (this.TriangleValue[i] === Math.min.apply(null, this.TriangleValue)) {
        this.TriangleChoosen = i;
      }
    }
  }
  // 2Ax + 2By = C => x = (C-2By)/2A
  // 2Dx + 2Ey = F => y = (F - 2D((C-2By)/2A))/2E
  defineLocation(arrayName: string[]) {
    let A = 0,
      B = 0,
      C = 0,
      D = 0,
      E = 0,
      F = 0;
    let location: number[][] = [[], [], []];
    let distance: number[] = [];
    for (let i = 0; i < this.NameTriangle[this.TriangleChoosen].length; i++) {
      for (let j = 0; j < this.database.length; j++) {
        if (
          !this.NameTriangle[this.TriangleChoosen][i].localeCompare(
            this.database[j].name
          )
        ) {
          location[i].push(this.database[j].location_x);
          location[i].push(this.database[j].location_y);
        }
      }
      for (let j = 0; j < arrayName.length; j++) {
        if (
          !this.NameTriangle[this.TriangleChoosen][i].localeCompare(
            arrayName[j]
          )
        ) {
          distance.push(this.distanceValue[j]);
        }
      }
    }
    console.log('loc: ', location);
    console.log('dis: ', distance);
    A = location[0][0] - location[1][0];
    B = location[0][1] - location[1][1];
    D = location[0][0] - location[2][0];
    E = location[0][1] - location[2][1];
    C =
      Math.pow(distance[1], 2) -
      Math.pow(distance[0], 2) +
      Math.pow(location[0][0], 2) -
      Math.pow(location[1][0], 2) +
      Math.pow(location[0][1], 2) -
      Math.pow(location[1][1], 2);
    F =
      Math.pow(distance[2], 2) -
      Math.pow(distance[0], 2) +
      Math.pow(location[0][0], 2) -
      Math.pow(location[2][0], 2) +
      Math.pow(location[0][1], 2) -
      Math.pow(location[2][1], 2);
    this.locationTrila[1] = (A * F - D * C) / (2 * A * E - 2 * D * B);
    this.locationTrila[0] = (C - 2 * B * this.locationTrila[1]) / (2 * A);
    // console.log('A= ', A);
    // console.log('B= ', B);
    // console.log('C= ', C);
    // console.log('D= ', D);
    // console.log('E= ', E);
    // console.log('F= ', F);
  }

  clearData() {
    this.TriangleValue = [];
    this.locationTrila = [];
    this.RSSFinal = [];
    this.RSS = [[], [], [], [], [], [], [], [], []];
    this.TriangleChoosen = 0;
    this.distanceValue = [];
  }
}
