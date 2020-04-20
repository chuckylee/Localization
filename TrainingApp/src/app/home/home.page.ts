import { Component } from '@angular/core';
import { DataService, Data } from 'src/app/services/data.service';

declare var WifiWizard2: any;
// const fakeData = [
//   {
//     id: 0,
//     info: [
//       {
//         name: 'wifi_1',
//         bssid: 'bssid_1',
//         level: '1',
//       },
//       {
//         name: 'wifi_1',
//         bssid: 'bssid_12',
//         level: '2',
//       },
//       {
//         name: 'wifi_2',
//         bssid: 'bssid_2',
//         level: '3',
//       },
//       {
//         name: 'wifi_3',
//         bssid: 'bssid_3',
//         level: '3',
//       },
//       {
//         name: 'wifi_4',
//         bssid: 'bssid_4',
//         level: '4',
//       },
//     ],
//   },
//   {
//     id: 1,
//     info: [
//       {
//         name: 'wifi_1',
//         bssid: 'bssid_12',
//         level: '4',
//       },
//       {
//         name: 'wifi_1',
//         bssid: 'bssid_1',
//         level: '23',
//       },

//       {
//         name: 'wifi_2',
//         bssid: 'bssid_2',
//         level: '3',
//       },
//       {
//         name: 'wifi_2',
//         bssid: 'bssid_22',
//         level: '33',
//       },
//       {
//         name: 'wifi_4',
//         bssid: 'bssid_4',
//         level: '4',
//       },
//       {
//         name: 'wifi_5',
//         bssid: 'bssid_5',
//         level: '5',
//       },
//     ],
//   },
//   {
//     id: 2,
//     info: [
//       {
//         name: 'wifi_5',
//         bssid: 'bssid_5',
//         level: '8',
//       },
//       {
//         name: 'wifi_2',
//         bssid: 'bssid_22',
//         level: '3',
//       },
//       {
//         name: 'wifi_2',
//         bssid: 'bssid_23',
//         level: '1',
//       },
//       {
//         name: 'wifi_1',
//         bssid: 'bssid_1',
//         level: '3',
//       },
//       {
//         name: 'wifi_4',
//         bssid: 'bssid_4',
//         level: '24',
//       },
//       {
//         name: 'wifi_3',
//         bssid: 'bssid_3',
//         level: '11',
//       },
//       {
//         name: 'wifi_6',
//         bssid: 'bssid_6',
//         level: '3',
//       },
//     ],
//   },
//   {
//     id: 3,
//     info: [
//       {
//         name: 'wifi1',
//         bssid: 'bssid1',
//         level: '123',
//       },
//       {
//         name: 'wifi1',
//         bssid: 'bssid12',
//         level: '224',
//       },

//       {
//         name: 'wifi4',
//         bssid: 'bssid4',
//         level: '244',
//       },
//       {
//         name: 'wifi5',
//         bssid: 'bssid5',
//         level: '245',
//       },
//     ],
//   },
// ];
@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  array_name: string[] = [];
  array_bssid: string[] = [];
  array_level: number[][] = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
  ];
  clear_bssid: string[] = [];
  clear_level: string[][] = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
  ];

  num_level: number[][] = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
  ];
  count_level: number[][] = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
  ];
  sum: number[] = [];
  y: number[] = [];
  o: number[] = [];
  RSS: number[][] = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
  ];
  RSS_final: number[] = [];

  arr: number[][] = [
    [-60, -61, -62, -66, -62, -66, -70, -70, -70],
    [-54, -54, -54, -54, -54],
    [-90],
    [-89, -89, -89],
    [-88, -91],
    [-89, -89],
  ];

  // fakeData = fakeData[0].info;

  id = 0;
  count = 0;
  countLevel = 0;
  results = [];
  info_txt = '';

  idea: Data = {
    name: [],
    bssid: [],
    location: [],
    level: [],
  };

  constructor(private dataService: DataService) {}
  ngOnInit() {}

  addIdea() {
    this.dataService.addIdea(this.idea).then(
      () => {
        console.log('Idea added');
      },
      (err) => {
        console.log('There was a problem adding your idea :(');
      }
    );
  }
  setDelay(i) {
    setTimeout(() => {
      this.getNetworks();
      this.count++;
      this.id++;
    }, 5000 * i);
  }

  click() {
    for (let i = 1; i <= 10; ++i) {
      this.setDelay(i);
    }
  }

  async getNetworks() {
    this.info_txt = 'loading...';
    try {
      let results = await WifiWizard2.scan();
      for (let item of results) {
        let level = parseInt(item.level);
        // console.log('name: ', item.SSID);
        // console.log('bssid: ', item.BSSID);
        // console.log('level: ', item.level);
        this.formatData(item.SSID, item.BSSID, level);
      }
      this.results = results;
      this.info_txt = '';
    } catch (error) {
      this.info_txt = error;
    }
  }

  print() {
    // this.id++;
    console.log('----------------------');
    let name_lenght = this.array_bssid.length;
    for (let i = 0; i < name_lenght; i++) {
      console.log(
        this.array_name[i] +
          '  ' +
          this.array_bssid[i] +
          '  ' +
          this.RSS_final[i] +
          '   [' +
          this.array_level[i] +
          ']'
      );
    }
    console.log('----------------------');
    console.log('sum', this.sum);
    console.log('y', this.y);
    console.log('o', this.o);
    console.log('RSS', this.RSS);
    console.log('RSS_final', this.RSS_final);
  }

  formatData(name: string, bssid: string, level: number) {
    if (this.id == 1) {
      this.array_name.push(name);
      this.array_bssid.push(bssid);
      this.array_level[this.countLevel].push(level);
      this.countLevel++;
    } else {
      let bssid_current = this.array_bssid.length;
      let check = true;
      for (let i = 0; i < bssid_current; i++) {
        if (!bssid.localeCompare(this.array_bssid[i])) {
          this.array_level[i].push(level);
          check = false;
          break;
        }
      }
      if (check == true) {
        this.array_name.push(name);
        let k = this.array_name.length;
        this.array_bssid.push(bssid);
        this.array_level[k - 1].push(level);
      }
    }
  }

  // caculator() {
  //   for (let i = 0; i < this.arr.length; i++) {
  //     for (let j = 0; j < this.arr[i].length; j++) {
  //       if (this.sum[i] == null) {
  //         this.sum[i] = this.arr[i][j];
  //       } else {
  //         this.sum[i] = this.sum[i] + this.arr[i][j];
  //       }
  //     }
  //     this.y[i] = this.sum[i] / this.arr[i].length;
  //   }

  //   for (let i = 0; i < this.arr.length; i++) {
  //     for (let j = 0; j < this.arr[i].length; j++) {
  //       if (this.o[i] == null) {
  //         this.o[i] =
  //           (this.arr[i][j] - this.y[i]) * (this.arr[i][j] - this.y[i]);
  //       } else {
  //         this.o[i] =
  //           this.o[i] +
  //           (this.arr[i][j] - this.y[i]) * (this.arr[i][j] - this.y[i]);
  //       }
  //     }
  //     this.o[i] = Math.sqrt(this.o[i] / (this.arr[i].length - 1));
  //   }

  //   for (let i = 0; i < this.arr.length; i++) {
  //     for (let j = 0; j < this.arr[i].length; j++) {
  //       if (
  //         this.arr[i][j] > this.y[i] - this.o[i] &&
  //         this.arr[i][j] < this.y[i] + this.o[i]
  //       ) {
  //         if (this.RSS[i][0] == null) {
  //           this.RSS[i][0] = this.arr[i][j];
  //         } else {
  //           let check = false;
  //           for (let k = 0; k < this.RSS[i].length; k++) {
  //             if (this.RSS[i][k] == this.arr[i][j]) {
  //               check = true;
  //               break;
  //             }
  //           }
  //           if (check == false) {
  //             this.RSS[i].push(this.arr[i][j]);
  //           }
  //         }
  //       }
  //     }
  //   }

  //   for (let i = 0; i < this.RSS.length; i++) {
  //     for (let j = 0; j < this.RSS[i].length; j++) {
  //       if (this.RSS_final[i] == null) {
  //         this.RSS_final[i] = this.RSS[i][j];
  //       } else {
  //         this.RSS_final[i] = this.RSS_final[i] + this.RSS[i][j];
  //       }
  //     }
  //     this.RSS_final[i] = this.RSS_final[i] / this.RSS[i].length;
  //   }

  //   for (let i = 0; i < this.arr.length; i++) {
  //     if (this.o[i] == 0) {
  //       this.RSS_final[i] = this.arr[i][0];
  //     }
  //     if (this.arr[i].length == 1) {
  //       this.RSS_final[i] = this.arr[i][0];
  //     }
  //   }
  // }

  caculator() {
    for (let i = 0; i < this.array_bssid.length; i++) {
      for (let j = 0; j < this.array_level[i].length; j++) {
        if (this.sum[i] == null) {
          this.sum[i] = this.array_level[i][j];
        } else {
          this.sum[i] = this.sum[i] + this.array_level[i][j];
        }
      }
      this.y[i] = this.sum[i] / this.array_level[i].length;
    }

    for (let i = 0; i < this.array_bssid.length; i++) {
      for (let j = 0; j < this.array_level[i].length; j++) {
        if (this.o[i] == null) {
          this.o[i] =
            (this.array_level[i][j] - this.y[i]) *
            (this.array_level[i][j] - this.y[i]);
        } else {
          this.o[i] =
            this.o[i] +
            (this.array_level[i][j] - this.y[i]) *
              (this.array_level[i][j] - this.y[i]);
        }
      }
      this.o[i] = Math.sqrt(this.o[i] / (this.array_level[i].length - 1));
    }

    for (let i = 0; i < this.array_bssid.length; i++) {
      for (let j = 0; j < this.array_level[i].length; j++) {
        if (
          this.array_level[i][j] > this.y[i] - this.o[i] &&
          this.array_level[i][j] < this.y[i] + this.o[i]
        ) {
          if (this.RSS[i][0] == null) {
            this.RSS[i][0] = this.array_level[i][j];
          } else {
            let check = false;
            for (let k = 0; k < this.RSS[i].length; k++) {
              if (this.RSS[i][k] == this.array_level[i][j]) {
                check = true;
                break;
              }
            }
            if (check == false) {
              this.RSS[i].push(this.array_level[i][j]);
            }
          }
        }
      }
    }

    for (let i = 0; i < this.RSS.length; i++) {
      for (let j = 0; j < this.RSS[i].length; j++) {
        if (this.RSS_final[i] == null) {
          this.RSS_final[i] = this.RSS[i][j];
        } else {
          this.RSS_final[i] = this.RSS_final[i] + this.RSS[i][j];
        }
      }
      this.RSS_final[i] = this.RSS_final[i] / this.RSS[i].length;
    }

    for (let i = 0; i < this.array_bssid.length; i++) {
      if (this.o[i] == 0) {
        this.RSS_final[i] = this.array_level[i][0];
      }
      if (this.array_level[i].length == 1) {
        this.RSS_final[i] = this.array_level[i][0];
      }
    }

    this.idea.name = this.array_name;
    this.idea.bssid = this.array_bssid;
    this.idea.level = this.RSS_final;
  }
}
