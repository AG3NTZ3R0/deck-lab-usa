import { useState, useEffect } from "react";
import type { Schema } from "../amplify/data/resource";
import { generateClient } from "aws-amplify/data";

const client = generateClient<Schema>();

export default function TodoList() {
  const [cards, setCards] = useState<Schema["Cards"]["type"][]>([]);

  const fetchCards = async () => {
    const { data: items } = await client.models.Cards.list();
    setCards(items);
  };

  useEffect(() => {
    fetchCards();
  }, []);

  return (
    <div>
      <ul>
        {cards.map(({ id, name }) => (
          <li key={id}>{name}</li>
        ))}
      </ul>
    </div>
  );
}
