import tkinter as tk

loc_language = "ru"

localization_labels = {
    "ru": {
        0: "Параметры",
        1: "Результат",
        2: "Поколение",
        3: "Вся популяция",
        4: "Количество магов",
        5: "Количество маглов",
        6: "Процент магов",
        7: "Процент маглов",
        31: "Начальная популяция",
        32: "Процент магов от начальной популяции (от 0 до 1)",
        33: "Количество поколений",
        34: "Процент магов создающих семью с \nмаглами в каждом поколении (от 0 до 1)",
        35: "Среднее число детей в семье магл-магл",
        36: "Среднее число детей в семье маг-магл",
        37: "Среднее число детей в семье маг-маг",
        38: "Вероятность рождения мага в семье маг-магл (от 0 до 1)"

    },
    "eng": {
        0: "Parameters",
        1: "Result",
        2: "Generation",
        3: "Total Population",
        4: "Number of Wizards",
        5: "Number of Muggles",
        6: "Percentage of Wizards",
        7: "Percentage of Muggles",
        31: "Initial Population",
        32: "Percentage of Wizards from initial population (from 0 to 1)",
        33: "Number of Generations",
        34: "Percentage of magicians creating a family \nwith Muggles in each generation (from 0 to 1)",
        35: "Average number of children in a Muggle-Muggle family",
        36: "Average number of children in a Wizard-Muggle family",
        37: "Average number of children in a Wizard-Wizard family",
        38: "The probability of a Wizard being born into a Muggle family (from 0 to 1)"
    }
}


class Population:
    def __init__(self, num_people, wizard_percentage, *, wizard_muggle_families, avg_wizard_wizard_child_count,
                 avg_wizard_muggle_child_count, avg_muggle_muggle_child_count, prob_of_wizard_birth):
        self.wizard_num = int(num_people * wizard_percentage)
        self.muggle_num = num_people - self.wizard_num
        self.generations = list((self.wizard_num, self.muggle_num))
        # процент магов образовавших семью с людьми
        self.wizard_muggle_families = wizard_muggle_families
        # среднее количество детей на семью магов
        self.avg_wizard_wizard_child_count = avg_wizard_wizard_child_count
        # среднее количество детей на семью маг + магл
        self.avg_wizard_muggle_child_count = avg_wizard_muggle_child_count
        # среднее количество детей на семью магл + магл
        self.avg_muggle_muggle_child_count = avg_muggle_muggle_child_count
        # вероятность рождения мага в семье маг + магл
        self.prob_of_wizard_birth = prob_of_wizard_birth

    def next_generation(self):
        new_wizard = 0
        new_muggle = 0

        # Маги плюс люди:
        num_of_wizard_muggle_families = min(self.wizard_num * self.wizard_muggle_families, self.muggle_num)
        new_wizard += int(
            num_of_wizard_muggle_families * self.avg_wizard_muggle_child_count * self.prob_of_wizard_birth
        )
        new_muggle += int(
            num_of_wizard_muggle_families * self.avg_wizard_muggle_child_count * (1 - self.prob_of_wizard_birth)
        )

        # Маги плюч маги:
        num_of_wizard_wizard_families = (self.wizard_num - num_of_wizard_muggle_families) // 2
        new_wizard += int(num_of_wizard_wizard_families * self.avg_wizard_wizard_child_count)

        # Люди плюс люди:
        num_of_muggle_muggle_families = (self.muggle_num - num_of_wizard_muggle_families) // 2
        new_muggle += int(num_of_muggle_muggle_families * self.avg_muggle_muggle_child_count)

        self.muggle_num = new_muggle
        self.wizard_num = new_wizard

        self.generations.append((self.muggle_num, self.wizard_num))

    def display_statistics(self):
        def format_numbers(number) -> str:
            ans = ''
            if number > 1_000_000:
                number = number/1_000_000
                ans = f"{number:,.1f}kk"
            elif number > 1_000:
                number = number/1_000
                ans = f"{number:,.1f}k"
            else:
                ans = f"{number:,.0f}"

            return ans

        population = self.wizard_num + self.muggle_num
        stats = {localization_labels[loc_language][3]: format_numbers(population),
                 localization_labels[loc_language][4]: format_numbers(self.wizard_num),
                 localization_labels[loc_language][5]: format_numbers(self.muggle_num),
                 localization_labels[loc_language][6]: f"{((self.wizard_num / population) * 100):.2f}%",
                 localization_labels[loc_language][7]: f"{((self.muggle_num / population) * 100):.2f}%"}
        return stats


class PopulationApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Population Statistics")
        self.geometry("1200x600+200+200")

        self.font = ("Arial", 20)
        self.entry_width = 15

        self.population = None

        self.create_widgets()
        self.locale_change_button = tk.Button(self, text="eng/ru", width=10, command=self.change_locale)
        self.locale_change_button.pack(side=tk.BOTTOM, pady=3)

    def create_widgets(self):
        # Параметры
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.params_frame = tk.Frame(self.main_frame)
        # Label
        tk.Label(self.params_frame, text=localization_labels[loc_language][0], font=self.font).pack(pady=3)

        params_labels_frame = tk.Frame(self.params_frame)
        params_labels_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def make_label(text):
            tk.Label(params_labels_frame, text=text, font=self.font, height=2).pack(fill=tk.BOTH, expand=True)

        params_entry_frame = tk.Frame(self.params_frame)
        params_entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def make_entry():
            return tk.Entry(params_entry_frame, font=self.font, width=self.entry_width, justify="center")

        # Labels
        make_label(localization_labels[loc_language][31])
        make_label(localization_labels[loc_language][32])
        make_label(localization_labels[loc_language][33])
        make_label(localization_labels[loc_language][34])
        make_label(localization_labels[loc_language][35])
        make_label(localization_labels[loc_language][36])
        make_label(localization_labels[loc_language][37])
        make_label(localization_labels[loc_language][38])

        # Entry
        self.ent_population = make_entry()
        self.ent_population.insert(0, "1_000_000")
        self.ent_population.pack(fill=tk.BOTH, expand=True)

        self.ent_magic_percentage = make_entry()
        self.ent_magic_percentage.insert(0, "0.01")
        self.ent_magic_percentage.pack(fill=tk.BOTH, expand=True)

        self.ent_generations = make_entry()
        self.ent_generations.insert(0, "5")
        self.ent_generations.pack(fill=tk.BOTH, expand=True)

        self.ent_wizard_muggle_families = make_entry()
        self.ent_wizard_muggle_families.insert(0, "0.7")
        self.ent_wizard_muggle_families.pack(fill=tk.BOTH, expand=True)

        self.ent_avg_muggle_muggle_child_count = make_entry()
        self.ent_avg_muggle_muggle_child_count.insert(0, "2.2")
        self.ent_avg_muggle_muggle_child_count.pack(fill=tk.BOTH, expand=True)

        self.ent_avg_wizard_muggle_child_count = make_entry()
        self.ent_avg_wizard_muggle_child_count.insert(0, "2.2")
        self.ent_avg_wizard_muggle_child_count.pack(fill=tk.BOTH, expand=True)

        self.ent_avg_wizard_wizard_child_count = make_entry()
        self.ent_avg_wizard_wizard_child_count.insert(0, "2.2")
        self.ent_avg_wizard_wizard_child_count.pack(fill=tk.BOTH, expand=True)

        self.ent_prob_of_wizard_birth = make_entry()
        self.ent_prob_of_wizard_birth.insert(0, "0.9")
        self.ent_prob_of_wizard_birth.pack(fill=tk.BOTH, expand=True)

        self.params_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Output Frame
        self.output_frame = tk.Frame(self.main_frame)

        # Label
        tk.Label(self.output_frame, text=localization_labels[loc_language][1], font=self.font).pack(pady=3)

        # Result Text
        self.result_text = tk.Text(self.output_frame, height=10, width=20, font=self.font)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Button
        self.generate_button = tk.Button(self.output_frame, text="Generate", width=20,
                                         command=self.generate_statistics, font=self.font)
        self.generate_button.pack(pady=7)

        self.output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def change_locale(self):
        global loc_language
        if loc_language == "eng":
            loc_language = "ru"
        else:
            loc_language = "eng"

        self.main_frame.destroy()
        self.create_widgets()

    def generate_statistics(self):
        # Get input values
        initial_population = int(self.ent_population.get())
        magic_percentage = float(self.ent_magic_percentage.get())
        generations = int(self.ent_generations.get())
        wizard_muggle_families = float(self.ent_wizard_muggle_families.get())
        avg_muggle_muggle_child_count = float(self.ent_avg_muggle_muggle_child_count.get())
        avg_wizard_muggle_child_count = float(self.ent_avg_wizard_muggle_child_count.get())
        avg_wizard_wizard_child_count = float(self.ent_avg_wizard_wizard_child_count.get())
        prob_of_wizard_birth = float(self.ent_prob_of_wizard_birth.get())

        # Create population object
        self.population = Population(initial_population, magic_percentage,
                                     wizard_muggle_families=wizard_muggle_families,
                                     avg_muggle_muggle_child_count=avg_muggle_muggle_child_count,
                                     avg_wizard_muggle_child_count=avg_wizard_muggle_child_count,
                                     avg_wizard_wizard_child_count=avg_wizard_wizard_child_count,
                                     prob_of_wizard_birth=prob_of_wizard_birth)

        # Generate statistics for each generation
        stats_text = ""
        for i in range(generations):
            self.population.next_generation()
            stats = self.population.display_statistics()
            stats_text += f"{localization_labels[loc_language][2]} {i + 1}:\n"
            for key, value in stats.items():
                stats_text += f"{key}: {value}\n"
            stats_text += "\n"

        # Display statistics
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, stats_text)


if __name__ == "__main__":
    app = PopulationApp()
    app.mainloop()
