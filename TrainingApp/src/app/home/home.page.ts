import { Component } from '@angular/core';
import { DataService, Data } from 'src/app/services/data.service';

declare var WifiWizard2: any;
const fakeData = [
  {
    id: 0,
    info: [
      {
        name: 'wifi_1',
        bssid: 'bssid_1',
        level: '1',
      },
      {
        name: 'wifi_1',
        bssid: 'bssid_12',
        level: '2',
      },
      {
        name: 'wifi_2',
        bssid: 'bssid_2',
        level: '3',
      },
      {
        name: 'wifi_3',
        bssid: 'bssid_3',
        level: '3',
      },
      {
        name: 'wifi_4',
        bssid: 'bssid_4',
        level: '4',
      },
    ],
  },
  {
    id: 1,
    info: [
      {
        name: 'wifi_1',
        bssid: 'bssid_12',
        level: '4',
      },
      {
        name: 'wifi_1',
        bssid: 'bssid_1',
        level: '23',
      },

      {
        name: 'wifi_2',
        bssid: 'bssid_2',
        level: '3',
      },
      {
        name: 'wifi_2',
        bssid: 'bssid_22',
        level: '33',
      },
      {
        name: 'wifi_4',
        bssid: 'bssid_4',
        level: '4',
      },
      {
        name: 'wifi_5',
        bssid: 'bssid_5',
        level: '5',
      },
    ],
  },
  {
    id: 2,
    info: [
      {
        name: 'wifi_5',
        bssid: 'bssid_5',
        level: '8',
      },
      {
        name: 'wifi_2',
        bssid: 'bssid_22',
        level: '3',
      },
      {
        name: 'wifi_2',
        bssid: 'bssid_23',
        level: '1',
      },
      {
        name: 'wifi_1',
        bssid: 'bssid_1',
        level: '3',
      },
      {
        name: 'wifi_4',
        bssid: 'bssid_4',
        level: '24',
      },
      {
        name: 'wifi_3',
        bssid: 'bssid_3',
        level: '11',
      },
      {
        name: 'wifi_6',
        bssid: 'bssid_6',
        level: '3',
      },
    ],
  },
  {
    id: 3,
    info: [
      {
        name: 'wifi1',
        bssid: 'bssid1',
        level: '123',
      },
      {
        name: 'wifi1',
        bssid: 'bssid12',
        level: '224',
      },

      {
        name: 'wifi4',
        bssid: 'bssid4',
        level: '244',
      },
      {
        name: 'wifi5',
        bssid: 'bssid5',
        level: '245',
      },
    ],
  },
];
@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  array_name: string[] = [];
  array_bssid: string[] = [];
  array_level: string[][] = [
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
  count_level: string[][] = [
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

  fakeData = fakeData[0].info;

  id = 0;
  count = 0;
  countLevel = 0;
  results = [];
  info_txt = '';

  idea: Data = {
    name: [],
    bssid: [],
    // level: [[]],
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
    for (let i = 1; i <= 5; ++i) {
      this.setDelay(i);
    }
  }

  async getNetworks() {
    this.info_txt = 'loading...';
    try {
      let results = await WifiWizard2.scan();
      for (let item of results) {
        console.log('name: ', item.SSID);
        console.log('bssid: ', item.BSSID);
        console.log('level: ', item.level);
        this.caculator(item.SSID, item.BSSID, item.level);
      }
      this.results = results;
      this.info_txt = '';
    } catch (error) {
      this.info_txt = error;
    }
  }

  filter(name: string, bssid: string, level: string) {
    this.array_name.push(name);
    this.array_bssid.push(bssid);
    this.array_level[this.id].push(level);
  }
  add() {
    this.fakeData = fakeData[this.id].info;
  }

  push() {
    let name_lenght = fakeData[this.id].info.length;
    if (this.id == 0) {
      for (let i = 0; i < name_lenght; i++) {
        this.array_name.push(fakeData[this.id].info[i].name);
        this.array_bssid.push(fakeData[this.id].info[i].bssid);
        this.array_level[i].push(fakeData[this.id].info[i].level);
      }
    } else {
      let bssid_current = this.array_bssid.length;
      let bssid_change = fakeData[this.id].info.length;
      console.log('bssid_current: ', bssid_current);
      console.log('bssid_change: ', bssid_change);
      for (let i = 0; i < bssid_change; i++) {
        let check = true;
        let temp = fakeData[this.id].info[i].bssid;
        for (let j = 0; j < bssid_current; j++) {
          if (!temp.localeCompare(this.array_bssid[j])) {
            this.array_level[j].push(fakeData[this.id].info[i].level);
            check = false;
            break;
          }
        }

        if (check == true) {
          this.array_name.push(fakeData[this.id].info[i].name);
          let k = this.array_name.length;
          this.array_bssid.push(fakeData[this.id].info[i].bssid);
          this.array_level[k - 1].push(fakeData[this.id].info[i].level);
        }
      }
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
          '   [' +
          this.array_level[i] +
          ']'
      );
    }
    console.log('----------------------');
    // console.log('name: ', this.array_name);
    // console.log('bssid: ', this.array_bssid);
    // console.log('level: ', this.array_level);
  }

  caculator(name: string, bssid: string, level: string) {
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
}
