import { useState, useEffect } from "react";
import type { Schema } from "../amplify/data/resource";
import { generateClient } from "aws-amplify/data";
import './Cards.css';
import { Crosshair, Crown, Diamond, Star } from 'lucide-react';

const client = generateClient<Schema>();

export default function Cards() {
  const [cards, setCards] = useState<Schema["Cards"]["type"][]>([]);
  const [stats, setStats] = useState({
    total: 0,
    diamond1: 0,
    diamond2: 0,
    diamond3: 0,
    diamond4: 0,
    star1: 0,
    star2: 0,
    star3: 0,
    crown1: 0
  });

  const fetchCards = async () => {
    const { data: items } = await client.models.Cards.list();
    setCards(items);

    const stats = {
      total: items.length,
      diamond1: items.filter(item => item.rarity === "1 Diamond").length,
      diamond2: items.filter(item => item.rarity === "2 Diamond").length,
      diamond3: items.filter(item => item.rarity === "3 Diamond").length,
      diamond4: items.filter(item => item.rarity === "4 Diamond").length,
      star1: items.filter(item => item.rarity === "1 Star").length,
      star2: items.filter(item => item.rarity === "2 Star").length,
      star3: items.filter(item => item.rarity === "3 Star").length,
      crown1: items.filter(item => item.rarity === "1 Crown").length
    };
    setStats(stats);
  };

  useEffect(() => {
    fetchCards();
  }, []);

  return (
    <div>
      <table className="quick-stats">
        <tbody>
          <tr>
            <th>
              <Crosshair className="pokeball"/>
            </th> <td>{stats.total}</td>
            <th>
              <Diamond className="diamond"/>
            </th> <td>{stats.diamond1}</td>
            <th>
              <Diamond className="diamond"/> 
              <Diamond className="diamond"/>
            </th> <td>{stats.diamond2}</td>
            <th>
              <Diamond className="diamond"/> 
              <Diamond className="diamond"/> 
              <Diamond className="diamond"/>
            </th> <td>{stats.diamond3}</td>
            <th>
              <Diamond className="diamond"/> 
              <Diamond className="diamond"/> 
              <Diamond className="diamond"/> 
              <Diamond className="diamond"/>
            </th> <td>{stats.diamond4}</td>
            <th>
              <Star className="star"/>
            </th> <td>{stats.star1}</td>
            <th>
              <Star className="star"/>
              <Star className="star"/>
            </th> <td>{stats.star2}</td>
            <th>
              <Star className="star"/>
              <Star className="star"/>
              <Star className="star"/>
            </th> <td>{stats.star3}</td>
            <th>
              <Crown className="crown"/>
            </th> <td>{stats.crown1}</td>
          </tr>
        </tbody>
      </table>
      <table className="pokemon-table">
        <thead> 
          <tr> 
            <th>ID</th> 
            <th>Name</th> 
            <th>Expansion</th> 
            <th>Pack</th> 
            <th>Rarity</th> 
            <th>Card 1-3</th> 
            <th>Card 4</th> 
            <th>Card 5</th> 
          </tr>
        </thead>
        <tbody>
        {
          cards.map(({ id, expansion, name, rarity }) => (
            <tr className={expansion!.pack}> 
              <td>{id}</td> 
              <td>{name}</td> 
              <td>{expansion!.name}</td> 
              <td>{expansion!.pack}</td> 
              <td>{rarity}</td>
              <td>{(expansion!.rates!.card1To3 * 100).toFixed(2)}%</td> 
              <td>{(expansion!.rates!.card4 * 100).toFixed(2)}%</td>
              <td>{(expansion!.rates!.card5 * 100).toFixed(2)}%</td>
            </tr>
          ))
        }
        </tbody>
      </table>
    </div>
  );
}
