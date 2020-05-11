import { Component } from '@angular/core';
import { DataService, Data } from 'src/app/services/data.service';
import { AlertController } from '@ionic/angular';

declare var WifiWizard2: any;

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

  constructor(
    private dataService: DataService,
    public alertController: AlertController
  ) {}
  ngOnInit() {}

  async UpdateDatabaseSuccess() {
    const alert = await this.alertController.create({
      header: 'Update Success',
    });

    await alert.present();
  }

  async UpdateDatabaseFail() {
    const alert = await this.alertController.create({
      header: 'Update Fail',
    });

    await alert.present();
  }
  addIdea() {
    this.dataService.addIdea(this.idea).then(
      () => {
        this.UpdateDatabaseSuccess();
        console.log('Idea added');
      },
      (err) => {
        this.UpdateDatabaseFail();
        console.log('There was a problem adding your idea :(');
      }
    );
  }
  setDelay(i) {
    setTimeout(() => {
      if (i < 11) {
        this.count++;
        this.id++;
        this.getNetworks();
      } else if (i == 11) {
        this.caculator();
        this.print();
      } else if (i == 12) {
        this.addIdea();
        this.clearData();
      }
    }, 5000 * i);
  }

  click() {
    for (let i = 1; i <= 12; ++i) {
      this.setDelay(i);
    }
  }

  async getNetworks() {
    this.info_txt = 'loading...';
    try {
      let results = await WifiWizard2.scan();
      for (let item of results) {
        // if (
        //   !item.SSID.localeCompare('Le Duc Thanh') ||
        //   !item.SSID.localeCompare('DaiDuong1') ||
        //   !item.SSID.localeCompare('Nhat Quynh') ||
        //   !item.SSID.localeCompare('Tang tret')
        // ) {
        let level = parseInt(item.level);
        this.formatData(item.SSID, item.BSSID, level);
        this.results = results;
        // }
      }

      this.info_txt = '';
    } catch (error) {
      this.info_txt = error;
    }
  }

  print() {
    console.log('----------------------');
    let name_lenght = this.array_bssid.length;
    for (let i = 0; i < name_lenght; i++) {
      console.log(
        'Real Data:  ',
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

  clearData() {
    this.id = 0;
    this.count = 0;
    this.countLevel = 0;
    this.array_name = [];
    this.array_bssid = [];
    this.array_level = [
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
    this.sum = [];
    this.y = [];
    this.o = [];
    this.RSS = [
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
    this.RSS_final = [];
    console.log('CLEAR DONE');
  }
}
