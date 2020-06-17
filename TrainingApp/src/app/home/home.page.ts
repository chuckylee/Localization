import { Component, ɵsetCurrentInjector, OnInit } from '@angular/core';
import { DataService, Data } from 'src/app/services/data.service';
import { AlertController } from '@ionic/angular';
import { map } from 'rxjs/operators';
import {
  AngularFirestore,
  AngularFirestoreCollection,
} from '@angular/fire/firestore';
import { Observable } from 'rxjs';

declare var WifiWizard2: any;

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  arrayName: string[] = [];
  arrayBssid: string[] = [];
  arrayLevel: number[][] = [[], [], [], [], [], [], [], []];
  sum: number[] = [];
  y: number[] = [];
  o: number[] = [];
  RSS: number[][] = [[], [], [], [], [], [], [], []];
  RSSFinal: number[] = [];
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
  infoTxt = '';
  idea: Data = {
    name: [],
    bssid: [],
    location: [],
    level: [],
    distance: null,
  };
  a = [];
  postsCol: AngularFirestoreCollection<Data>;
  posts: Observable<Data[]>;
  newposts: Observable<Data[]>;
  constructor(
    private dataService: DataService,
    public alertController: AlertController,
    private afs: AngularFirestore
  ) {
    // console.log(this.a.length);
  }

  ngOnInit() {
    // this.dataService
    //   .getList()
    //   .snapshotChanges()
    //   .pipe(
    //     map((changes) =>
    //       changes.map((c) => ({
    //         // key: c.payload.doc.id,
    //         // ...c.payload.doc.data(),
    //       }))
    //     )
    //   )
    //   .subscribe((datas) => {
    //     console.log(datas);
    //   });
    this.postsCol = this.afs.collection('cities');
    this.posts = this.postsCol.valueChanges();
    this.postsCol.snapshotChanges().subscribe((data) => {
      data.forEach((change) => {
        if (change.type === 'added') {
          console.log(change.payload.doc.id);
          console.log(change.payload.doc.data());
        }
      });
    });

    // this.posts.subscribe((data) => {
    //   console.log(data);
    // });
  }

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
        this.print();
      } else if (i === 12) {
        this.caculator();
        this.print();
      } else if (i === 13) {
        this.addIdea();
      }
    }, 2000 * i);
  }

  // click() {
  //   this.clearData();
  //   for (let i = 1; i <= 100; ++i) {
  //     this.setDelay2(i);
  //   }
  //   setTimeout(() => {
  //     this.caculator();
  //   }, 101000);
  //   setTimeout(() => {
  //     this.print();
  //     this.addIdea();
  //   }, 102000);
  // }
  click() {
    this.clearData();
    for (let i = 1; i <= 6; i++) {
      this.setDelay(i);
    }
  }

  // setDelay(i) {
  //   setTimeout(() => {
  //     if (i < 4) {
  //       for (let j = 1; j <= 30; ++j) {
  //         this.setDelay2(j);
  //       }
  //     } else if (i === 5) {
  //       this.caculator();
  //       this.print();
  //     } else if (i === 6) {
  //       this.addIdea();
  //     }
  //   }, 5000 * i);
  // }

  setDelay2(i) {
    setTimeout(() => {
      this.count++;
      this.id++;
      this.getNetworks();
      // console.log('hi');
    }, 1000 * i);
  }
  async getNetworks() {
    this.infoTxt = 'loading...';
    try {
      // tslint:disable-next-line:prefer-const
      let results = await WifiWizard2.scan();
      // tslint:disable-next-line:prefer-const
      for (let item of results) {
        if (
          !item.SSID.localeCompare('UTS_709_IoT_1') ||
          !item.SSID.localeCompare('UTS_709_IoT_2') ||
          !item.SSID.localeCompare('ESP32-1') ||
          !item.SSID.localeCompare('ESP32-2') ||
          !item.SSID.localeCompare('ESP32-3') ||
          !item.SSID.localeCompare('ESP32-4') ||
          !item.SSID.localeCompare('ESP32-5')
        ) {
          // tslint:disable-next-line:prefer-const
          let level = parseInt(item.level);
          this.formatData(item.SSID, item.BSSID, level);
          console.log(this.count + ': ' + item.SSID + ' , ' + item.level);
          this.results = results;
        }
      }

      this.infoTxt = '';
    } catch (error) {
      this.infoTxt = error;
    }
  }

  print() {
    console.log('----------------------');
    // tslint:disable-next-line:prefer-const
    let nameLenght = this.arrayBssid.length;
    for (let i = 0; i < nameLenght; i++) {
      console.log(
        'Real Data:  ',
        this.arrayName[i] +
        '  ' +
        this.arrayBssid[i] +
        '  ' +
        this.RSSFinal[i] +
        '   [' +
        this.arrayLevel[i] +
        ']'
      );
    }
    // console.log('----------------------');
    // console.log('sum', this.sum);
    // console.log('y', this.y);
    // console.log('o', this.o);
    // console.log('RSS', this.RSS);
    // console.log('RSSFinal', this.RSSFinal);
  }

  formatData(name: string, bssid: string, level: number) {
    if (this.id === 1) {
      this.arrayName.push(name);
      this.arrayBssid.push(bssid);
      this.arrayLevel[this.countLevel].push(level);
      this.countLevel++;
    } else {
      // tslint:disable-next-line:prefer-const
      let bssidCurrent = this.arrayBssid.length;
      let check = true;
      for (let i = 0; i < bssidCurrent; i++) {
        if (!bssid.localeCompare(this.arrayBssid[i])) {
          this.arrayLevel[i].push(level);
          check = false;
          break;
        }
      }
      if (check === true) {
        this.arrayName.push(name);
        // tslint:disable-next-line:prefer-const
        let k = this.arrayName.length;
        this.arrayBssid.push(bssid);
        this.arrayLevel[k - 1].push(level);
      }
    }
  }

  caculator() {
    for (let i = 0; i < this.arrayBssid.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < this.arrayLevel[i].length; j++) {
        if (this.sum[i] == null) {
          this.sum[i] = this.arrayLevel[i][j];
        } else {
          this.sum[i] = this.sum[i] + this.arrayLevel[i][j];
        }
      }
      this.y[i] = this.sum[i] / this.arrayLevel[i].length;
    }

    for (let i = 0; i < this.arrayBssid.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < this.arrayLevel[i].length; j++) {
        if (this.o[i] == null) {
          this.o[i] =
            (this.arrayLevel[i][j] - this.y[i]) *
            (this.arrayLevel[i][j] - this.y[i]);
        } else {
          this.o[i] =
            this.o[i] +
            (this.arrayLevel[i][j] - this.y[i]) *
            (this.arrayLevel[i][j] - this.y[i]);
        }
      }
      this.o[i] = Math.sqrt(this.o[i] / (this.arrayLevel[i].length - 1));
    }

    for (let i = 0; i < this.arrayBssid.length; i++) {
      // tslint:disable-next-line:prefer-for-of
      for (let j = 0; j < this.arrayLevel[i].length; j++) {
        if (
          this.arrayLevel[i][j] > this.y[i] - this.o[i] &&
          this.arrayLevel[i][j] < this.y[i] + this.o[i]
        ) {
          if (this.RSS[i][0] == null) {
            this.RSS[i][0] = this.arrayLevel[i][j];
          } else {
            let check = false;
            // tslint:disable-next-line:prefer-for-of
            for (let k = 0; k < this.RSS[i].length; k++) {
              if (this.RSS[i][k] === this.arrayLevel[i][j]) {
                check = true;
                break;
              }
            }
            if (check === false) {
              this.RSS[i].push(this.arrayLevel[i][j]);
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

    for (let i = 0; i < this.arrayBssid.length; i++) {
      if (this.o[i] === 0) {
        this.RSSFinal[i] = this.arrayLevel[i][0];
      }
      if (this.arrayLevel[i].length === 1) {
        this.RSSFinal[i] = this.arrayLevel[i][0];
      }
    }

    this.idea.name = this.arrayName;
    this.idea.bssid = this.arrayBssid;
    this.idea.level = this.RSSFinal;
  }

  clearData() {
    this.id = 0;
    this.count = 0;
    this.countLevel = 0;
    this.arrayName = [];
    this.arrayBssid = [];
    this.arrayLevel = [[], [], [], [], [], [], [], []];
    this.sum = [];
    this.y = [];
    this.o = [];
    this.RSS = [[], [], [], [], [], [], [], []];
    this.RSSFinal = [];
    console.log('CLEAR DONE');
  }
}
