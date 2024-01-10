class KingdomRelations:
    def __init__(self):
        self.relations = {}
        self.vote_counts = {"ghaniyar": {"vaali": 3, "gurung": 3, "cheeka": 3, "ranga": 3, "narang": 3, "vishnu": 3},
                            "mannar": {"shiva_mannar": 0, "raja_mannar": 15, "varadha_raj_mannar": 1,
                                       "baachi": 0, "rudra": 1, "radha_rama": 0, "om": 1}}

        # Adding initial relationships
        self.add_relation("dhaara", "devaratha_raisaar", "father")
        self.add_relation("baarava", "raja_mannar", "son_in_law")
        self.add_relation("baarava", "radha_rama", "husband")
        self.add_relation("shiva_mannar", "raja_mannar", "father")
        self.add_relation("raja_mannar", "varadha_raj_mannar", "second_wife_son")
        self.add_relation("raja_mannar", "baachi", "second_wife_son")
        self.add_relation("raja_mannar", "rudra", "first_wife_son")
        self.add_relation("raja_mannar", "radha_rama", "first_wife_daughter")
        self.add_relation("raja_mannar", "om", "first_wife_brother")
        self.add_relation("narang", "vishnu", "son")

        # Adding all relationships
        self.add_relation("dhaara", "devaratha_raisaar", "father")
        self.add_relation("dhaara", "baarava", "father")
        self.add_relation("dhaara", "dheera", "father")

        self.add_relation("devaratha_raisaar", "dhaara", "child")
        self.add_relation("devaratha_raisaar", "baarava", "sibling")
        self.add_relation("devaratha_raisaar", "dheera", "sibling")

        self.add_relation("baarava", "dhaara", "child")
        self.add_relation("baarava", "devaratha_raisaar", "sibling")
        self.add_relation("baarava", "radha_rama", "husband")
        self.add_relation("baarava", "raja_mannar", "son_in_law")
        self.add_relation("baarava", "rudra", "son_in_law")

        self.add_relation("dheera", "dhaara", "child")
        self.add_relation("dheera", "devaratha_raisaar", "sibling")

        self.add_relation("shiva_mannar", "raja_mannar", "father")
        self.add_relation("shiva_mannar", "rudra", "father")

        self.add_relation("raja_mannar", "shiva_mannar", "child")
        self.add_relation("raja_mannar", "varadha_raj_mannar", "second_wife_son")
        self.add_relation("raja_mannar", "baachi", "second_wife_son")
        self.add_relation("raja_mannar", "rudra", "first_wife_son")
        self.add_relation("raja_mannar", "radha_rama", "first_wife_daughter")
        self.add_relation("raja_mannar", "om", "first_wife_brother")
        self.add_relation("raja_mannar", "baarava", "father_in_law")
        self.add_relation("raja_mannar", "radha_rama", "father_in_law")

        self.add_relation("varadha_raj_mannar", "raja_mannar", "father")
        self.add_relation("varadha_raj_mannar", "rudra", "brother")
        self.add_relation("varadha_raj_mannar", "radha_rama", "brother")
        self.add_relation("varadha_raj_mannar", "om", "brother")

        self.add_relation("baachi", "raja_mannar", "father")
        self.add_relation("baachi", "rudra", "brother")
        self.add_relation("baachi", "radha_rama", "sister")
        self.add_relation("baachi", "om", "brother")

        self.add_relation("rudra", "raja_mannar", "father")
        self.add_relation("rudra", "varadha_raj_mannar", "brother")
        self.add_relation("rudra", "radha_rama", "sister")
        self.add_relation("rudra", "baachi", "brother")

        self.add_relation("radha_rama", "raja_mannar", "father")
        self.add_relation("radha_rama", "varadha_raj_mannar", "brother")
        self.add_relation("radha_rama", "rudra", "brother")
        self.add_relation("radha_rama", "om", "brother")
        self.add_relation("radha_rama", "baarava", "wife")

        self.add_relation("om", "raja_mannar", "brother")
        self.add_relation("om", "varadha_raj_mannar", "brother")
        self.add_relation("om", "rudra", "brother")
        self.add_relation("om", "radha_rama", "brother")

        self.add_relation("vishnu", "narang", "child")
        self.add_relation("vishnu", "ghaniyar", "child")

    def add_relation(self, person1, person2, relationship):
        self.relations.setdefault(person1, {})[person2] = relationship
        self.relations.setdefault(person2, {})[person1] = relationship

    def get_relationship(self, person1, person2):
        if person1 in self.relations and person2 in self.relations[person1]:
            return self.relations[person1][person2]
        else:
            return "No relationship found."

    def get_vote_count(self, tribe, person):
        if tribe.lower() in self.vote_counts and person.lower() in self.vote_counts[tribe.lower()]:
            return self.vote_counts[tribe.lower()][person.lower()]
        else:
            return "Invalid tribe or person."

# Example usage:
if __name__ == "__main__":
    salaar_relations = KingdomRelations()

    # Example relationships
    # print(salaar_relations.get_relationship(c))
    print(salaar_relations.get_relationship("baarava", "raja_mannar"))
    print(salaar_relations.get_relationship("baarava", "radha_rama"))
    print(salaar_relations.get_relationship("shiva_mannar", "raja_mannar"))

    # Example vote counts
    print(salaar_relations.get_vote_count("ghaniyar", "vishnu"))
    print(salaar_relations.get_vote_count("mannar", "shiva_mannar"))
